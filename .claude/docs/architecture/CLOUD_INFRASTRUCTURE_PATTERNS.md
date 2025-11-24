# Cloud Infrastructure Patterns for Scalable APIs with Databases

## Executive Summary

This document provides production-ready cloud infrastructure patterns for building scalable APIs with databases. It covers multi-tier architecture, load balancing, connection pooling, and caching strategies for both AWS and GCP environments.

---

## 1. Multi-Tier Architecture Patterns

### 1.1 Classic Three-Tier Architecture (Recommended for Most APIs)

```
┌─────────────────────────────────────────────────────────┐
│                    CDN Layer (CloudFlare)                │
│              (Static assets, DDoS protection)            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│               Load Balancer Tier                         │
│  AWS ALB / NLB / GCP Cloud Load Balancer               │
│  - HTTPS termination                                    │
│  - SSL/TLS management                                   │
│  - Path-based routing                                   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│           Application Server Tier                       │
│  (Auto-scaling group of API servers)                   │
│  - Docker containers (ECS/GKE)                         │
│  - Horizontal scaling (5-500 instances)                │
│  - Health checks every 30 seconds                      │
│  - Multi-AZ deployment (3+ availability zones)         │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│            Caching Layer Tier                           │
│  - Redis/Memcached (in-memory store)                   │
│  - Distributed cache (replicated, 3+ nodes)           │
│  - 99.99% uptime SLA requirement                       │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│           Data Persistence Tier                         │
│  - Primary database (Read/Write operations)            │
│  - Read replicas (Read-only, 2-5 replicas)           │
│  - Automated failover (10-30 second RTO)              │
│  - Encryption at rest (AES-256)                        │
└─────────────────────────────────────────────────────────┘
```

### 1.2 AWS Implementation (Multi-Tier)

```yaml
AWS_Architecture:
  Region: us-east-1
  Availability_Zones:
    - us-east-1a
    - us-east-1b
    - us-east-1c

  CDN_Layer:
    Service: CloudFront
    Origin: ALB
    Behaviors:
      - Static_Assets:
          Pattern: "/*.{js,css,png,jpg,gif,svg}"
          Cache_TTL: 86400  # 24 hours
          Compress: true
      - API_Requests:
          Pattern: "/api/*"
          Cache_TTL: 0  # No caching for dynamic content
          Compress: true

  Load_Balancing_Tier:
    Service: Application Load Balancer (ALB)
    Configuration:
      Listeners:
        - Port: 443
          Protocol: HTTPS
          SSL_Policy: "ELBSecurityPolicy-TLS-1-2-2017-01"
          Certificate: "arn:aws:acm:..."
        - Port: 80
          Protocol: HTTP
          Action: Redirect to HTTPS

      Target_Groups:
        - Name: api-servers
          Protocol: HTTP
          Port: 8000
          Health_Check:
            Path: /health
            Interval_Seconds: 30
            Timeout_Seconds: 5
            Healthy_Threshold: 2
            Unhealthy_Threshold: 3
          Stickiness:
            Enabled: false  # Stateless APIs don't need sticky sessions
            Duration: null

  Application_Tier:
    Service: ECS on EC2 or Fargate
    Cluster: api-cluster
    Task_Definition:
      Family: api-task
      Memory: 512  # MB
      CPU: 256     # CPU units
      Containers:
        - Name: api
          Image: "123456789.dkr.ecr.us-east-1.amazonaws.com/api:latest"
          Port_Mappings:
            - Container_Port: 8000
              Protocol: tcp
          Environment:
            DATABASE_URL: "postgresql://user:pass@db-cluster.xxx.rds.amazonaws.com:5432/api"
            REDIS_URL: "redis://api-cache.xxx.ng.0001.use1.cache.amazonaws.com:6379"
          Log_Configuration:
            Log_Driver: awslogs
            Options:
              awslogs-group: "/ecs/api"
              awslogs-region: "us-east-1"
              awslogs-stream-prefix: "ecs"

    Auto_Scaling:
      Min_Capacity: 3
      Desired_Capacity: 5
      Max_Capacity: 50
      Target_Tracking_Scaling_Policy:
        Target_CPU_Utilization: 70%
        Target_Memory_Utilization: 80%
        Scale_Out_Cooldown: 60  # seconds
        Scale_In_Cooldown: 300  # seconds

    Deployment_Strategy:
      Type: rolling
      Minimum_Healthy_Percent: 100
      Maximum_Percent: 200  # Allows 2x capacity during deployment

  Caching_Tier:
    Service: ElastiCache (Redis)
    Engine: redis
    Engine_Version: "7.0"
    Node_Type: cache.r7g.xlarge  # 32 GB memory
    Number_Cache_Clusters: 3
    Automatic_Failover: true
    Multi_AZ: true
    Transit_Encryption: true
    At_Rest_Encryption: true
    Subnet_Group: api-cache-subnet-group
    Security_Group: api-cache-sg
    Parameter_Group:
      Family: redis7
      Parameters:
        maxmemory-policy: "allkeys-lru"  # LRU eviction policy
        timeout: 300
        tcp-keepalive: 60

  Database_Tier:
    Service: RDS (PostgreSQL)
    Engine: postgres
    Engine_Version: "15.3"
    Instance_Class: db.r6i.2xlarge  # 64 GB RAM, optimized for reads
    Multi_AZ: true
    Storage:
      Type: gp3
      Allocated: 1000  # GB
      Max_Allocated: 5000  # GB for autoscaling
      IOPS: 3000
      Throughput: 125  # MB/s

    Backup_Configuration:
      Backup_Retention_Period: 30  # days
      Backup_Window: "02:00-03:00"  # UTC
      Copy_Backups_To_Region: us-west-2  # Disaster recovery

    Read_Replicas:
      - Instance_Class: db.r6i.xlarge
        Availability_Zone: us-east-1b
      - Instance_Class: db.r6i.xlarge
        Availability_Zone: us-east-1c

    Performance_Insights:
      Enabled: true
      Retention_Period: 7  # days

    Enhanced_Monitoring:
      Monitor_Interval: 60  # seconds
      IAM_Role: "arn:aws:iam::..."

    Encryption:
      Storage_Encryption: true
      KMS_Key: "arn:aws:kms:..."
```

### 1.3 GCP Implementation (Multi-Tier)

```yaml
GCP_Architecture:
  Project_ID: my-api-project
  Region: us-central1
  Zones:
    - us-central1-a
    - us-central1-b
    - us-central1-c

  CDN_Layer:
    Service: Cloud CDN
    Backend_Services:
      - Name: api-backend
        Protocol: HTTPS
        Port: 443
        Cache_Mode: "CACHE_ALL_STATIC"
        Default_TTL: 3600
        Max_TTL: 86400

  Load_Balancing_Tier:
    Service: Cloud Load Balancing (HTTP(S))
    Frontend:
      Protocol: HTTPS
      Port: 443
      SSL_Certificates:
        - "projects/my-project/global/sslCertificates/my-cert"
      SSL_Policy: "google-optimized-ssl-policy"

    Backend_Service:
      Name: api-backend
      Protocol: HTTP
      Port: 8000
      Health_Checks:
        - Name: api-health-check
          Path: /health
          Check_Interval_Sec: 30
          Timeout_Sec: 5
          Healthy_Threshold: 2
          Unhealthy_Threshold: 3
      Session_Affinity: CLIENT_IP  # For stateful services only
      Affinity_Cookie_TTL_Sec: 1800
      Connection_Draining:
        Draining_Timeout_Sec: 300
      Timeout_Sec: 30

  Application_Tier:
    Service: GKE (Google Kubernetes Engine)
    Cluster:
      Name: api-cluster
      Zone: us-central1
      Node_Pools:
        - Name: default
          Initial_Node_Count: 3
          Autoscaling:
            Min_Node_Count: 3
            Max_Node_Count: 50
          Machine_Type: n2-standard-4  # 4 vCPU, 16 GB RAM
          Boot_Disk_Size_GB: 100
          Disk_Type: pd-ssd

    Kubernetes_Deployment:
      API_Version: apps/v1
      Kind: Deployment
      Metadata:
        Name: api
        Namespace: default
      Spec:
        Replicas: 5
        Strategy:
          Type: RollingUpdate
          RollingUpdate:
            Max_Surge: "25%"
            Max_Unavailable: 0
        Selector:
          Match_Labels:
            App: api
        Template:
          Metadata:
            Labels:
              App: api
          Spec:
            Containers:
              - Name: api
                Image: "gcr.io/my-project/api:latest"
                Ports:
                  - Container_Port: 8000
                Env:
                  - Name: DATABASE_URL
                    Value: "postgresql://cloudsql-proxy:5432/api"
                  - Name: REDIS_URL
                    Value: "redis://redis-cluster.default.svc.cluster.local:6379"
                Resources:
                  Requests:
                    Memory: "256Mi"
                    CPU: "250m"
                  Limits:
                    Memory: "512Mi"
                    CPU: "500m"
                Readiness_Probe:
                  HTTP_Get:
                    Path: /health
                    Port: 8000
                  Initial_Delay_Seconds: 10
                  Period_Seconds: 30
                Liveness_Probe:
                  HTTP_Get:
                    Path: /health
                    Port: 8000
                  Initial_Delay_Seconds: 30
                  Period_Seconds: 60

            # GKE specific: Cloud SQL Proxy sidecar
            Init_Containers:
              - Name: cloud-sql-proxy
                Image: "gcr.io/cloudsql-docker/cloud-sql-proxy:1.33.2"
                Args:
                  - "my-project:us-central1:api-db"
                  - "-ip_address_types=PRIVATE"
                Security_Context:
                  Run_As_Non_Root: true

  Caching_Tier:
    Service: Memorystore for Redis
    Tier: standard  # or premium for high availability
    Size_GB: 30
    Region: us-central1
    Authorize_Networks:
      - Name: api-cluster
        CIDR: "10.0.0.0/8"  # GKE cluster CIDR
    Auth_Enabled: true
    Transit_Encryption_Mode: SERVER_AUTHENTICATION
    Persistence:
      Enabled: true
      Rdb_Snapshot_Period: TWELVE_HOURS

  Database_Tier:
    Service: Cloud SQL (PostgreSQL)
    Database_Version: POSTGRES_15
    Tier: db-custom-8-32768  # 8 vCPU, 32 GB RAM
    Region: us-central1
    Availability_Type: REGIONAL  # High availability
    Storage:
      Type: PD_SSD
      Size_GB: 1000
      Auto_Expand:
        Enabled: true
        Max_Size_GB: 5000

    Backup_Configuration:
      Enabled: true
      Start_Time: "02:00"
      Location: us
      Backup_Kind: AUTOMATED
      Point_In_Time_Recovery_Enabled: true
      Transaction_Log_Retention_Days: 7

    Read_Replicas:
      - Name: api-db-replica-1
        Region: us-central1
        Availability_Type: ZONAL
      - Name: api-db-replica-2
        Region: us-east1
        Availability_Type: ZONAL

    Insights_Config:
      Query_Insights_Enabled: true
      Query_Plans_Per_Minute: 5
      Query_String_Length: 1024
      Record_Application_Tags: true

    IP_Configuration:
      Ipv4_Enabled: false  # Private IP only
      Private_Network: "projects/my-project/global/networks/api-network"
      Authorized_Networks: []  # Use Private IP instead
```

---

## 2. Load Balancing Strategy

### 2.1 Load Balancer Configuration (AWS ALB)

```python
# load_balancer_config.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class HealthCheckConfig:
    """Health check configuration for load balancer"""
    path: str = "/health"
    interval_seconds: int = 30
    timeout_seconds: int = 5
    healthy_threshold: int = 2
    unhealthy_threshold: int = 3
    matcher: str = "200-299"

@dataclass
class LoadBalancerConfig:
    """Production load balancer configuration"""

    # Basic Configuration
    name: str
    listeners: List[Dict] = None
    target_groups: List[Dict] = None

    # Health Check
    health_check: HealthCheckConfig = None

    # Advanced Features
    enable_deletion_protection: bool = True
    enable_cross_zone_load_balancing: bool = True
    enable_http2: bool = True
    enable_http: bool = False  # Redirect to HTTPS only

    # Sticky Sessions (for stateful APIs only)
    enable_stickiness: bool = False
    stickiness_duration: int = 86400  # 24 hours

    def __post_init__(self):
        if self.health_check is None:
            self.health_check = HealthCheckConfig()

        if self.listeners is None:
            self.listeners = self._default_listeners()

        if self.target_groups is None:
            self.target_groups = self._default_target_groups()

    def _default_listeners(self) -> List[Dict]:
        """Default listener configuration"""
        return [
            {
                "Protocol": "HTTPS",
                "Port": 443,
                "DefaultActions": [{
                    "Type": "forward",
                    "TargetGroupArn": "arn:aws:elasticloadbalancing:..."
                }],
                "Certificates": [{
                    "CertificateArn": "arn:aws:acm:..."
                }],
                "SslPolicy": "ELBSecurityPolicy-TLS-1-2-2017-01"
            },
            {
                "Protocol": "HTTP",
                "Port": 80,
                "DefaultActions": [{
                    "Type": "redirect",
                    "RedirectConfig": {
                        "Protocol": "HTTPS",
                        "Port": "443",
                        "StatusCode": "HTTP_301"
                    }
                }]
            }
        ]

    def _default_target_groups(self) -> List[Dict]:
        """Default target group configuration"""
        return [
            {
                "Name": "api-servers",
                "Protocol": "HTTP",
                "Port": 8000,
                "VpcId": "vpc-xxxxx",
                "HealthCheckProtocol": "HTTP",
                "HealthCheckPath": self.health_check.path,
                "HealthCheckIntervalSeconds": self.health_check.interval_seconds,
                "HealthCheckTimeoutSeconds": self.health_check.timeout_seconds,
                "HealthyThresholdCount": self.health_check.healthy_threshold,
                "UnhealthyThresholdCount": self.health_check.unhealthy_threshold,
                "Matcher": {"HttpCode": self.health_check.matcher},
                "TargetType": "ip",  # For ECS/Fargate
                "DeregistrationDelay": {
                    "TimeoutSeconds": 300  # Connection draining
                },
                "Stickiness": {
                    "Enabled": self.enable_stickiness,
                    "Type": "lb_cookie",
                    "LbCookieDurationSeconds": self.stickiness_duration
                } if self.enable_stickiness else None,
                "TargetGroupAttributes": [
                    {
                        "Key": "deregistration_delay.timeout_seconds",
                        "Value": "300"
                    },
                    {
                        "Key": "slow_start.duration_seconds",
                        "Value": "60"  # Ramp-up time for new targets
                    },
                    {
                        "Key": "preserve_client_ip.enabled",
                        "Value": "true"
                    }
                ]
            }
        ]

# Advanced: Path-based routing
PATH_BASED_ROUTING = {
    "Rules": [
        {
            "Priority": 1,
            "Conditions": [{
                "Field": "path-pattern",
                "Values": ["/api/v1/*"]
            }],
            "Actions": [{
                "Type": "forward",
                "TargetGroupArn": "arn:aws:elasticloadbalancing:.../targetgroup/api-v1/..."
            }]
        },
        {
            "Priority": 2,
            "Conditions": [{
                "Field": "path-pattern",
                "Values": ["/api/v2/*"]
            }],
            "Actions": [{
                "Type": "forward",
                "TargetGroupArn": "arn:aws:elasticloadbalancing:.../targetgroup/api-v2/..."
            }]
        },
        {
            "Priority": 3,
            "Conditions": [{
                "Field": "host-header",
                "Values": ["admin.api.example.com"]
            }],
            "Actions": [{
                "Type": "forward",
                "TargetGroupArn": "arn:aws:elasticloadbalancing:.../targetgroup/admin/..."
            }]
        }
    ]
}

# Advanced: Weighted routing (canary deployments)
WEIGHTED_ROUTING = {
    "Rules": [
        {
            "Priority": 1,
            "Conditions": [{
                "Field": "path-pattern",
                "Values": ["/api/*"]
            }],
            "Actions": [{
                "Type": "forward",
                "ForwardConfig": {
                    "TargetGroups": [
                        {
                            "TargetGroupArn": "arn:aws:elasticloadbalancing:.../targetgroup/api-stable/...",
                            "Weight": 95  # 95% of traffic
                        },
                        {
                            "TargetGroupArn": "arn:aws:elasticloadbalancing:.../targetgroup/api-canary/...",
                            "Weight": 5   # 5% of traffic (new version)
                        }
                    ],
                    "StickynessConfig": {
                        "Enabled": True,
                        "DurationSeconds": 3600
                    }
                }
            }]
        }
    ]
}
```

### 2.2 Advanced Load Balancing: Global Traffic Management

```python
# global_load_balancing.py
from enum import Enum
from typing import Dict, List

class RoutingPolicy(Enum):
    GEOLOCATION = "geolocation"      # Route based on geographic location
    LATENCY = "latency"               # Route to lowest latency endpoint
    WEIGHTED = "weighted"             # Route by weight percentage
    FAILOVER = "failover"             # Primary/secondary failover
    MULTI_VALUE = "multi_value"       # Multiple healthy endpoints

class GlobalLoadBalancingConfig:
    """
    Multi-region load balancing with Route53 (AWS)
    or Cloud DNS (GCP)
    """

    def __init__(self):
        self.regions = {
            "us-east-1": {
                "endpoint": "api-us-east-1.example.com",
                "health_check_id": "health-check-us-east-1",
                "weight": 50,
                "latency_region": "us-east-1"
            },
            "eu-west-1": {
                "endpoint": "api-eu-west-1.example.com",
                "health_check_id": "health-check-eu-west-1",
                "weight": 30,
                "latency_region": "eu-west-1"
            },
            "ap-southeast-1": {
                "endpoint": "api-ap-southeast-1.example.com",
                "health_check_id": "health-check-ap-southeast-1",
                "weight": 20,
                "latency_region": "ap-southeast-1"
            }
        }

    def geolocation_routing(self) -> Dict:
        """Route based on user geography"""
        return {
            "HostedZoneId": "Z1234567890ABC",
            "Name": "api.example.com",
            "Type": "A",
            "ResourceRecordSets": [
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": "US-Users",
                    "GeoLocation": {
                        "CountryCode": "US"
                    },
                    "AliasTarget": {
                        "HostedZoneId": "Z35SXDOTRQ7X7K",  # ALB zone
                        "DNSName": "api-us-east-1.example.com",
                        "EvaluateTargetHealth": True
                    },
                    "TTL": 300
                },
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": "EU-Users",
                    "GeoLocation": {
                        "ContinentCode": "EU"
                    },
                    "AliasTarget": {
                        "HostedZoneId": "Z32O12XQLNTSW2",  # ALB zone
                        "DNSName": "api-eu-west-1.example.com",
                        "EvaluateTargetHealth": True
                    },
                    "TTL": 300
                },
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": "APAC-Users",
                    "GeoLocation": {
                        "ContinentCode": "AS"
                    },
                    "AliasTarget": {
                        "HostedZoneId": "Z1LMS91P8CMLE5",  # ALB zone
                        "DNSName": "api-ap-southeast-1.example.com",
                        "EvaluateTargetHealth": True
                    },
                    "TTL": 300
                },
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": "Default",
                    "GeoLocation": {
                        "CountryCode": "*"
                    },
                    "AliasTarget": {
                        "HostedZoneId": "Z35SXDOTRQ7X7K",
                        "DNSName": "api-us-east-1.example.com",
                        "EvaluateTargetHealth": True
                    },
                    "TTL": 300
                }
            ]
        }

    def latency_routing(self) -> Dict:
        """Route to lowest latency endpoint"""
        return {
            "HostedZoneId": "Z1234567890ABC",
            "Name": "api.example.com",
            "Type": "A",
            "ResourceRecordSets": [
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": f"{region}-latency",
                    "Region": region,
                    "AliasTarget": {
                        "HostedZoneId": zone_id,
                        "DNSName": config["endpoint"],
                        "EvaluateTargetHealth": True
                    },
                    "TTL": 60  # Lower TTL for latency-based routing
                }
                for region, zone_id, config in [
                    ("us-east-1", "Z35SXDOTRQ7X7K", self.regions["us-east-1"]),
                    ("eu-west-1", "Z32O12XQLNTSW2", self.regions["eu-west-1"]),
                    ("ap-southeast-1", "Z1LMS91P8CMLE5", self.regions["ap-southeast-1"])
                ]
            ]
        }

    def failover_routing(self) -> Dict:
        """Primary/secondary failover configuration"""
        return {
            "HostedZoneId": "Z1234567890ABC",
            "Name": "api.example.com",
            "Type": "A",
            "ResourceRecordSets": [
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": "Primary",
                    "Failover": "PRIMARY",
                    "AliasTarget": {
                        "HostedZoneId": "Z35SXDOTRQ7X7K",
                        "DNSName": "api-us-east-1.example.com",
                        "EvaluateTargetHealth": True
                    },
                    "HealthCheckId": "health-check-us-east-1",
                    "TTL": 60
                },
                {
                    "Name": "api.example.com",
                    "Type": "A",
                    "SetIdentifier": "Secondary",
                    "Failover": "SECONDARY",
                    "AliasTarget": {
                        "HostedZoneId": "Z32O12XQLNTSW2",
                        "DNSName": "api-eu-west-1.example.com",
                        "EvaluateTargetHealth": True
                    },
                    "HealthCheckId": "health-check-eu-west-1",
                    "TTL": 60
                }
            ]
        }
```

---

## 3. Database Connection Pooling Configuration

### 3.1 Connection Pool Architecture

```python
# connection_pool_config.py
from dataclasses import dataclass
from typing import Optional, Dict
import os

@dataclass
class ConnectionPoolConfig:
    """Production connection pool configuration for PostgreSQL"""

    # Pool Sizing
    min_size: int = 10                    # Minimum idle connections
    max_size: int = 100                   # Maximum concurrent connections
    max_overflow: int = 20                # Additional connections beyond max_size
    pool_recycle: int = 3600              # Recycle connections after 1 hour

    # Timeouts
    connect_timeout: int = 10             # Connection creation timeout (seconds)
    idle_timeout: int = 900               # Close idle connections after 15 minutes
    max_lifetime: int = 3600              # Max connection lifetime (1 hour)
    statement_timeout: int = 30000        # Query timeout (milliseconds)

    # Health Checks
    pool_pre_ping: bool = True            # Verify connections before use
    echo: bool = False                    # Log all SQL statements
    echo_pool: bool = False               # Log pool operations

    # URL Configuration
    database_url: str = os.getenv("DATABASE_URL",
                                  "postgresql://user:pass@localhost:5432/dbname")

    # Advanced Options
    json_serializer: Optional[str] = None
    json_deserializer: Optional[str] = None

    # Connection Arguments
    connection_args: Dict = None

    def __post_init__(self):
        if self.connection_args is None:
            self.connection_args = {
                "connect_timeout": self.connect_timeout,
                "application_name": "api-server",
                "options": "-c statement_timeout=30000"
            }

# FastAPI/SQLAlchemy Implementation
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

class DatabaseConnection:
    """Production database connection manager"""

    def __init__(self, config: ConnectionPoolConfig):
        self.config = config
        self.engine = self._create_engine()

    def _create_engine(self):
        """Create SQLAlchemy engine with production settings"""
        return create_engine(
            self.config.database_url,

            # Pool configuration
            poolclass=QueuePool,
            pool_size=self.config.min_size,
            max_overflow=self.config.max_overflow,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=self.config.pool_pre_ping,
            pool_timeout=self.config.connect_timeout,

            # Execution options
            echo=self.config.echo,
            echo_pool=self.config.echo_pool,

            # Connection arguments
            connect_args=self.config.connection_args,

            # JSON support for PostgreSQL
            json_serializer=self.config.json_serializer,
            json_deserializer=self.config.json_deserializer,

            # Performance options
            isolation_level="READ_COMMITTED",
            future=True
        )

    def get_session(self):
        """Get database session"""
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        return Session()

    def health_check(self) -> bool:
        """Verify database connectivity"""
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
                return True
        except SQLAlchemyError as e:
            print(f"Database health check failed: {str(e)}")
            return False

# Alternative: Using asyncio with async_engine for better scalability
from sqlalchemy.ext.asyncio import create_async_engine

class AsyncDatabaseConnection:
    """Async database connection for high-concurrency APIs"""

    def __init__(self, config: ConnectionPoolConfig):
        self.config = config
        # Convert postgresql:// to postgresql+asyncpg://
        async_url = config.database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://"
        )
        self.engine = create_async_engine(
            async_url,
            poolclass=QueuePool,
            pool_size=self.config.min_size,
            max_overflow=self.config.max_overflow,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=self.config.pool_pre_ping,
            echo=self.config.echo,
            future=True
        )

    async def get_session(self):
        """Get async database session"""
        from sqlalchemy.ext.asyncio import AsyncSession
        return AsyncSession(self.engine)
```

### 3.2 PgBouncer - Connection Pool Proxy

```ini
# pgbouncer.ini - Production configuration
[databases]
; Format: database_name = host=localhost port=5432 user=postgres password=
api = host=rds-instance.xxx.amazonaws.com port=5432 user=api password=secure_password dbname=api_db

[pgbouncer]
; Listening socket
listen_addr = 0.0.0.0
listen_port = 6432
unix_socket_dir = /var/run/pgbouncer

; Authentication
auth_file = /etc/pgbouncer/userlist.txt
auth_type = md5

; Pool Management
pool_mode = transaction        ; transaction, session, or statement
max_client_conn = 1000         ; Max client connections
default_pool_size = 25         ; Pool size per database
min_pool_size = 10             ; Minimum idle connections
reserve_pool_size = 5          ; Connections reserved for superuser
reserve_pool_timeout = 3       ; Timeout for reserve pool

; Advanced tuning
server_lifetime = 3600         ; Recycle server connections after 1 hour
server_idle_timeout = 600      ; Close idle server connections after 10 min
server_connect_timeout = 15    ; Timeout for connecting to backend
server_login_retry = 15        ; Retry connecting every 15 seconds

; DNS management
dns_max_ttl = 15               ; Cache DNS results for 15 seconds
dns_zone_check_period = 0      ; Disable zone checks (if not using DNS)

; Query timeout
query_timeout = 0              ; No query timeout (handle in app)
query_wait_timeout = 120       ; Wait for available connection for 2 minutes

; Logging
syslog = 1
syslog_facility = LOG_LOCAL0
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
verbose = 1

; Statistics
stats_period = 60              ; Update stats every 60 seconds

; Server-side connection
tcp_keepalives = 1
tcp_keepalives_idle = 30
tcp_keepalives_interval = 10
```

### 3.3 PgBouncer Health Check and Deployment

```python
# pgbouncer_health_check.py
import psycopg2
import logging
from datetime import datetime

class PgBouncerHealthCheck:
    """Monitor PgBouncer connection pool health"""

    def __init__(self, pgbouncer_host='localhost', pgbouncer_port=6432):
        self.host = pgbouncer_host
        self.port = pgbouncer_port
        self.logger = logging.getLogger(__name__)

    def get_pool_stats(self) -> dict:
        """Get current pool statistics"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database='pgbouncer',
                user='postgres'
            )
            cur = conn.cursor()

            # Get pool statistics
            cur.execute("SHOW POOLS;")
            pools = cur.fetchall()

            # Get client statistics
            cur.execute("SHOW CLIENTS;")
            clients = cur.fetchall()

            # Get server statistics
            cur.execute("SHOW SERVERS;")
            servers = cur.fetchall()

            cur.close()
            conn.close()

            return {
                'pools': pools,
                'clients': clients,
                'servers': servers,
                'timestamp': datetime.utcnow()
            }
        except Exception as e:
            self.logger.error(f"Failed to get pool stats: {str(e)}")
            return None

    def check_connection_saturation(self, warning_threshold=80) -> bool:
        """Check if connection pool is approaching saturation"""
        stats = self.get_pool_stats()
        if not stats:
            return False

        total_connections = sum(row[3] for row in stats['pools'])  # cl_active
        max_connections = 1000  # From pgbouncer.ini

        utilization = (total_connections / max_connections) * 100

        if utilization > warning_threshold:
            self.logger.warning(f"Pool utilization at {utilization}%")
            return True

        return False

    def get_slow_connections(self, timeout_seconds=5) -> list:
        """Identify connections waiting longer than threshold"""
        stats = self.get_pool_stats()
        if not stats:
            return []

        slow_connections = []
        for client in stats['clients']:
            wait_time = (datetime.utcnow() - client[5]).total_seconds()
            if wait_time > timeout_seconds:
                slow_connections.append({
                    'type': client[0],
                    'address': client[1],
                    'port': client[2],
                    'wait_time': wait_time
                })

        return slow_connections

# Kubernetes deployment for PgBouncer
PGBOUNCER_K8S_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pgbouncer
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pgbouncer
  template:
    metadata:
      labels:
        app: pgbouncer
    spec:
      containers:
      - name: pgbouncer
        image: pgbouncer:1.16
        ports:
        - containerPort: 6432
          name: pgbouncer
        env:
        - name: DATABASES_HOST
          value: "rds-instance.xxx.amazonaws.com"
        - name: DATABASES_PORT
          value: "5432"
        - name: DATABASES_USER
          value: "api"
        - name: DATABASES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: pgbouncer-secrets
              key: database-password
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - psql -h localhost -p 6432 -d pgbouncer -c "SHOW STATS" | grep -q api
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - psql -h localhost -p 6432 -d pgbouncer -c "SHOW DATABASES" | grep -q api
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
        volumeMounts:
        - name: pgbouncer-config
          mountPath: /etc/pgbouncer
      volumes:
      - name: pgbouncer-config
        configMap:
          name: pgbouncer-config
---
apiVersion: v1
kind: Service
metadata:
  name: pgbouncer
spec:
  selector:
    app: pgbouncer
  ports:
  - name: pgbouncer
    port: 6432
    targetPort: 6432
  type: ClusterIP
"""
```

---

## 4. Caching Layer Design

### 4.1 Multi-Level Caching Strategy

```
┌─────────────────────────────────────────────┐
│     Level 1: Client-Side Caching             │
│  (Browser cache, Service Worker, LocalStorage)
│  TTL: 1 hour - 30 days                      │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│     Level 2: CDN Caching (CloudFront)        │
│  (Edge locations, geo-distributed)          │
│  TTL: 1 hour - 7 days                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Level 3: Application Cache (Redis)         │
│  (In-process, distributed, near-instant)    │
│  TTL: 5 minutes - 1 hour                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│    Level 4: Database Query Cache             │
│  (Query result caching)                     │
│  TTL: 30 seconds - 5 minutes                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Level 5: Database Page Cache               │
│  (Shared buffers, page cache)               │
│  Automatic (LRU eviction)                   │
└─────────────────────────────────────────────┘
```

### 4.2 Redis Caching Implementation

```python
# redis_cache_strategy.py
import redis
import json
from typing import Any, Optional, Callable
from functools import wraps
from datetime import timedelta
import hashlib

class RedisCache:
    """Production Redis caching layer"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0",
                 default_ttl: int = 3600):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {str(e)}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL"""
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Cache set error: {str(e)}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {str(e)}")
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache invalidate error: {str(e)}")
            return 0

    def cache_decorator(self, ttl: Optional[int] = None):
        """Decorator for automatic cache handling"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Generate cache key from function name and arguments
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)

                # Try to get from cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Call function if not cached
                result = func(*args, **kwargs)

                # Cache the result
                self.set(cache_key, result, ttl)

                return result

            return wrapper
        return decorator

    def _generate_cache_key(self, func_name: str, args: tuple,
                           kwargs: dict) -> str:
        """Generate cache key from function and arguments"""
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"cache:{func_name}:{key_hash}"

# FastAPI integration
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
cache = RedisCache(
    redis_url="redis://redis-cluster.default.svc.cluster.local:6379/0",
    default_ttl=300  # 5 minutes default
)

@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: str):
    """Get product with caching"""
    cache_key = f"product:{product_id}"

    # Try cache first
    cached_product = cache.get(cache_key)
    if cached_product:
        return JSONResponse({
            "data": cached_product,
            "source": "cache"
        })

    # Fetch from database
    # product = await db.get_product(product_id)

    # Cache the result (5 minute TTL)
    cache.set(cache_key, product, ttl=300)

    return JSONResponse({
        "data": product,
        "source": "database"
    })

@app.post("/api/v1/products/{product_id}")
async def update_product(product_id: str, data: dict):
    """Update product and invalidate cache"""
    # Update in database
    # product = await db.update_product(product_id, data)

    # Invalidate related cache keys
    cache_key = f"product:{product_id}"
    cache.delete(cache_key)
    cache.invalidate_pattern(f"products:*")  # Invalidate list caches

    return {"status": "updated"}

# Cache warming strategy
class CacheWarmer:
    """Pre-populate cache with frequently accessed data"""

    def __init__(self, cache: RedisCache):
        self.cache = cache

    async def warm_popular_products(self):
        """Warm cache with popular products"""
        # Get top 100 products from database
        # products = await db.get_popular_products(limit=100)

        # Cache each product (24 hour TTL)
        for product in products:
            cache_key = f"product:{product['id']}"
            self.cache.set(cache_key, product, ttl=86400)

    async def warm_user_sessions(self):
        """Warm cache with active user sessions"""
        # Get active sessions from database
        # sessions = await db.get_active_sessions()

        # Cache each session (1 hour TTL)
        for session in sessions:
            cache_key = f"session:{session['id']}"
            self.cache.set(cache_key, session, ttl=3600)

    async def warm_all(self):
        """Warm all critical caches"""
        await self.warm_popular_products()
        await self.warm_user_sessions()

# Cache invalidation patterns
class CacheInvalidationStrategy:
    """
    Strategies for cache invalidation:
    1. TTL-based: Automatic expiration
    2. Event-based: Invalidate on data change
    3. Pattern-based: Invalidate related keys
    4. Manual: Explicit invalidation
    """

    def __init__(self, cache: RedisCache):
        self.cache = cache

    def on_product_created(self, product_id: str):
        """Invalidate on product creation"""
        self.cache.invalidate_pattern("products:*")

    def on_product_updated(self, product_id: str):
        """Invalidate on product update"""
        self.cache.delete(f"product:{product_id}")
        self.cache.invalidate_pattern("products:*")

    def on_product_deleted(self, product_id: str):
        """Invalidate on product deletion"""
        self.cache.delete(f"product:{product_id}")
        self.cache.invalidate_pattern("products:*")

    def on_category_updated(self, category_id: str):
        """Invalidate category and all related products"""
        self.cache.delete(f"category:{category_id}")
        self.cache.invalidate_pattern(f"products:category:{category_id}:*")
```

### 4.3 Redis Cluster Configuration

```yaml
# redis-cluster-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-cluster-config
data:
  redis.conf: |
    # Redis Cluster Configuration for Production

    # Network
    port 6379
    bind 0.0.0.0
    protected-mode no
    tcp-backlog 511
    timeout 0
    tcp-keepalive 300

    # Cluster
    cluster-enabled yes
    cluster-config-file /data/nodes.conf
    cluster-node-timeout 15000

    # Memory Management
    maxmemory 32gb
    maxmemory-policy allkeys-lru

    # Persistence
    save 900 1            # Save if 1 key changed in 15 min
    save 300 10           # Save if 10 keys changed in 5 min
    save 60 10000         # Save if 10000 keys changed in 1 min

    rdbcompression yes
    rdbchecksum yes
    dbfilename dump.rdb
    dir /data

    # Replication
    repl-diskless-sync yes
    repl-diskless-sync-delay 5
    repl-disable-tcp-nodelay no
    repl-backlog-size 256mb

    # Logging
    loglevel notice
    logfile /var/log/redis/redis-server.log

    # Monitoring
    slowlog-log-slower-than 10000
    slowlog-max-len 128

    # Security
    requirepass your_secure_password
    masterauth your_secure_password

    # Clients
    maxclients 10000

    # Key eviction
    lazyfree-lazy-eviction yes
    lazyfree-lazy-expire yes

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
spec:
  serviceName: redis-cluster
  replicas: 6  # 3 master, 3 replica
  selector:
    matchLabels:
      app: redis-cluster
  template:
    metadata:
      labels:
        app: redis-cluster
    spec:
      containers:
      - name: redis
        image: redis:7.0-alpine
        command:
        - redis-server
        - /etc/redis/redis.conf
        - --cluster-announce-ip
        - $(POD_IP)
        env:
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        ports:
        - containerPort: 6379
          name: client
        - containerPort: 16379
          name: gossip
        volumeMounts:
        - name: data
          mountPath: /data
        - name: config
          mountPath: /etc/redis
        resources:
          requests:
            memory: "4Gi"
            cpu: "1000m"
          limits:
            memory: "8Gi"
            cpu: "2000m"
        livenessProbe:
          exec:
            command:
            - redis-cli
            - -p
            - "6379"
            - ping
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: config
        configMap:
          name: redis-cluster-config
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 100Gi
---
apiVersion: v1
kind: Service
metadata:
  name: redis-cluster
spec:
  clusterIP: None
  selector:
    app: redis-cluster
  ports:
  - port: 6379
    targetPort: 6379
    name: client
  - port: 16379
    targetPort: 16379
    name: gossip
```

### 4.4 Cache Performance Monitoring

```python
# cache_monitoring.py
import time
from typing import Dict
from dataclasses import dataclass

@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    avg_response_time: float = 0.0
    memory_usage: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0

class CacheMonitor:
    """Monitor Redis cache performance"""

    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.metrics = CacheMetrics()

    def get_redis_info(self) -> Dict:
        """Get Redis server info"""
        info = self.redis_client.info()
        return {
            'connected_clients': info['connected_clients'],
            'used_memory': info['used_memory'],
            'used_memory_human': info['used_memory_human'],
            'used_memory_peak': info['used_memory_peak_human'],
            'evicted_keys': info['evicted_keys'],
            'keyspace_hits': info['keyspace_hits'],
            'keyspace_misses': info['keyspace_misses'],
            'instantaneous_ops_per_sec': info['instantaneous_ops_per_sec'],
            'total_commands_processed': info['total_commands_processed']
        }

    def calculate_hit_rate(self) -> float:
        """Calculate actual cache hit rate from Redis"""
        info = self.get_redis_info()
        hits = info['keyspace_hits']
        misses = info['keyspace_misses']
        total = hits + misses
        return (hits / total * 100) if total > 0 else 0

    def get_slowest_keys(self, count: int = 10) -> list:
        """Identify slowest keys (by access time)"""
        # Note: Requires Redis Modules or application-level tracking
        pass

    def get_cache_stats(self) -> Dict:
        """Get comprehensive cache statistics"""
        info = self.get_redis_info()

        return {
            'status': 'healthy' if info['connected_clients'] > 0 else 'down',
            'connected_clients': info['connected_clients'],
            'memory': {
                'used': info['used_memory'],
                'used_human': info['used_memory_human'],
                'peak': info['used_memory_peak'],
                'peak_human': info['used_memory_peak_human']
            },
            'performance': {
                'hit_rate': self.calculate_hit_rate(),
                'hits': info['keyspace_hits'],
                'misses': info['keyspace_misses'],
                'evicted_keys': info['evicted_keys'],
                'ops_per_sec': info['instantaneous_ops_per_sec']
            },
            'commands': {
                'total_processed': info['total_commands_processed']
            }
        }

# Prometheus metrics export
from prometheus_client import Counter, Gauge, Histogram

cache_hits = Counter('cache_hits_total', 'Total cache hits')
cache_misses = Counter('cache_misses_total', 'Total cache misses')
cache_latency = Histogram('cache_latency_seconds', 'Cache operation latency')
redis_memory = Gauge('redis_memory_bytes', 'Redis memory usage')

class InstrumentedRedisCache(RedisCache):
    """Redis cache with Prometheus instrumentation"""

    def get(self, key: str) -> Optional[Any]:
        start_time = time.time()
        try:
            value = super().get(key)
            if value is not None:
                cache_hits.inc()
            else:
                cache_misses.inc()
            cache_latency.observe(time.time() - start_time)
            return value
        except Exception:
            cache_misses.inc()
            cache_latency.observe(time.time() - start_time)
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        start_time = time.time()
        result = super().set(key, value, ttl)
        cache_latency.observe(time.time() - start_time)

        # Update memory gauge
        info = self.redis_client.info()
        redis_memory.set(info['used_memory'])

        return result
```

---

## 5. Monitoring and Observability

### 5.1 CloudWatch/Datadog Dashboard

```python
# monitoring_setup.py
import boto3
from dataclasses import dataclass
from typing import List

@dataclass
class MetricThreshold:
    """Alert threshold configuration"""
    metric_name: str
    threshold: float
    comparison: str  # GreaterThanThreshold, LessThanThreshold
    evaluation_periods: int = 2
    period_seconds: int = 300

class ProductionMonitoring:
    """Setup comprehensive monitoring for production"""

    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')

    def create_api_dashboard(self):
        """Create CloudWatch dashboard for API metrics"""
        dashboard_body = {
            'Widgets': [
                {
                    'Type': 'Metric',
                    'Properties': {
                        'Metrics': [
                            ['AWS/ApplicationELB', 'TargetResponseTime', {'stat': 'Average'}],
                            ['AWS/ApplicationELB', 'RequestCount', {'stat': 'Sum'}],
                            ['AWS/ApplicationELB', 'HTTPCode_Target_2XX_Count', {'stat': 'Sum'}],
                            ['AWS/ApplicationELB', 'HTTPCode_Target_5XX_Count', {'stat': 'Sum'}],
                            ['AWS/ApplicationELB', 'HealthyHostCount', {'stat': 'Average'}],
                            ['AWS/ApplicationELB', 'UnHealthyHostCount', {'stat': 'Average'}]
                        ],
                        'Period': 60,
                        'Stat': 'Average',
                        'Region': 'us-east-1',
                        'Title': 'API Load Balancer Metrics'
                    }
                },
                {
                    'Type': 'Metric',
                    'Properties': {
                        'Metrics': [
                            ['AWS/ECS', 'CPUUtilization', {'stat': 'Average'}],
                            ['AWS/ECS', 'MemoryUtilization', {'stat': 'Average'}]
                        ],
                        'Period': 60,
                        'Stat': 'Average',
                        'Region': 'us-east-1',
                        'Title': 'ECS Container Metrics'
                    }
                },
                {
                    'Type': 'Metric',
                    'Properties': {
                        'Metrics': [
                            ['AWS/RDS', 'DatabaseConnections', {'stat': 'Average'}],
                            ['AWS/RDS', 'CPUUtilization', {'stat': 'Average'}],
                            ['AWS/RDS', 'ReadLatency', {'stat': 'Average'}],
                            ['AWS/RDS', 'WriteLatency', {'stat': 'Average'}],
                            ['AWS/RDS', 'DiskQueueDepth', {'stat': 'Average'}]
                        ],
                        'Period': 60,
                        'Stat': 'Average',
                        'Region': 'us-east-1',
                        'Title': 'RDS Database Metrics'
                    }
                },
                {
                    'Type': 'Metric',
                    'Properties': {
                        'Metrics': [
                            ['AWS/ElastiCache', 'CacheHits', {'stat': 'Sum'}],
                            ['AWS/ElastiCache', 'CacheMisses', {'stat': 'Sum'}],
                            ['AWS/ElastiCache', 'Evictions', {'stat': 'Sum'}],
                            ['AWS/ElastiCache', 'DatabaseMemoryUsagePercentage', {'stat': 'Average'}]
                        ],
                        'Period': 60,
                        'Stat': 'Average',
                        'Region': 'us-east-1',
                        'Title': 'Redis Cache Metrics'
                    }
                }
            ]
        }

        self.cloudwatch.put_dashboard(
            DashboardName='api-production-dashboard',
            DashboardBody=json.dumps(dashboard_body)
        )

    def create_alarms(self):
        """Create critical alarms"""
        alarms = [
            MetricThreshold(
                metric_name='TargetResponseTime',
                threshold=1.0,  # 1 second
                comparison='GreaterThanThreshold'
            ),
            MetricThreshold(
                metric_name='HTTPCode_Target_5XX_Count',
                threshold=10,
                comparison='GreaterThanThreshold'
            ),
            MetricThreshold(
                metric_name='UnHealthyHostCount',
                threshold=1,
                comparison='GreaterThanThreshold'
            ),
            MetricThreshold(
                metric_name='CPUUtilization',
                threshold=80,
                comparison='GreaterThanThreshold'
            ),
            MetricThreshold(
                metric_name='DatabaseConnections',
                threshold=80,  # Approaching max
                comparison='GreaterThanThreshold'
            )
        ]

        for alarm in alarms:
            self.cloudwatch.put_metric_alarm(
                AlarmName=f"api-{alarm.metric_name}",
                ComparisonOperator=alarm.comparison,
                EvaluationPeriods=alarm.evaluation_periods,
                MetricName=alarm.metric_name,
                Namespace='AWS/ApplicationELB',
                Period=alarm.period_seconds,
                Statistic='Average',
                Threshold=alarm.threshold,
                ActionsEnabled=True,
                AlarmActions=['arn:aws:sns:us-east-1:123456789:critical-alerts'],
                AlarmDescription=f"Alert when {alarm.metric_name} exceeds {alarm.threshold}"
            )
```

---

## 6. Deployment Checklist

### Pre-Production Deployment

- [ ] Load test API (minimum 1000 concurrent users)
- [ ] Validate database connection pooling (check pool saturation)
- [ ] Test cache invalidation strategies
- [ ] Verify failover and recovery procedures
- [ ] Run security scan (OWASP Top 10)
- [ ] Validate TLS/SSL certificates
- [ ] Test DNS failover
- [ ] Verify monitoring and alerting

### Post-Deployment

- [ ] Monitor error rates (< 0.1%)
- [ ] Monitor response times (p95 < 500ms, p99 < 1s)
- [ ] Monitor database connections (< 80% utilization)
- [ ] Monitor cache hit rate (> 80% for hot data)
- [ ] Review CloudWatch/Datadog dashboards hourly for first 24 hours

---

## References

- AWS ECS Best Practices
- PostgreSQL Connection Pooling Guide
- Redis High Availability
- Kubernetes Deployment Patterns

**Document Version:** 1.0
**Last Updated:** 2025-11-24
**Status:** Production Ready
