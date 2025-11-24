export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm lg:flex">
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
          <p className="text-4xl font-bold mb-8 text-center">
            Claude Code Project Template
          </p>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-3 lg:text-left gap-6">
        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className="mb-3 text-2xl font-semibold">
            Next.js Frontend{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              →
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            Production-ready Next.js 14 with App Router, TypeScript, and Tailwind CSS
          </p>
        </div>

        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className="mb-3 text-2xl font-semibold">
            FastAPI Backend{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              →
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            High-performance Python backend with FastAPI and async support
          </p>
        </div>

        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className="mb-3 text-2xl font-semibold">
            15 AI Agents{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              →
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            Specialized agent orchestration system for development workflows
          </p>
        </div>
      </div>

      <div className="mt-16 text-center">
        <h3 className="text-xl font-semibold mb-4">Quick Start</h3>
        <div className="bg-gray-900 text-gray-100 p-6 rounded-lg text-left font-mono text-sm max-w-2xl">
          <p className="text-green-400"># Install dependencies</p>
          <p className="mb-4">./setup.sh</p>

          <p className="text-green-400"># Start development</p>
          <p>npm run dev</p>
          <p className="mb-4">uvicorn main:app --reload</p>

          <p className="text-green-400"># Invoke your first agent</p>
          <p>@anand-2.0 help me get started</p>
        </div>
      </div>
    </main>
  )
}
