"use client";

import Link from "next/link";

export default function DashboardPage() {

  return (

    <div className="flex h-screen">

      {/* Sidebar */}
      <div className="w-64 bg-black text-white p-6">

        <h1 className="text-2xl font-bold mb-8">
          ODIN
        </h1>

        <div className="flex flex-col gap-4">

          <Link href="/dashboard">
            Dashboard
          </Link>

          <Link href="/chat">
            Chat
          </Link>

          <Link href="/graph">
            Knowledge Graph
          </Link>

          <Link href="/learning">
            Learning Analytics
          </Link>

        </div>

      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">

        <h2 className="text-3xl font-bold">
          Welcome to ODIN
        </h2>

        <p className="mt-4 text-gray-600">

          Your cognitive operating system.

        </p>

      </div>

    </div>
  );
}