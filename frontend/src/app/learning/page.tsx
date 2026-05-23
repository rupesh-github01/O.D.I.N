"use client";

import {
  useEffect,
  useState
} from "react";

export default function LearningPage() {

  const [overview, setOverview] =
    useState<any>(null);

  useEffect(() => {

    fetchOverview();

  }, []);

  async function fetchOverview() {

    try {

      const response = await fetch(
        "http://localhost:8000/analytics/overview"
      );

      const data =
        await response.json();

      setOverview(data);

    } catch (error) {

      console.error(error);

    }
  }

  if (!overview) {

    return (
      <div className="bg-black text-white min-h-screen p-6">

        Loading analytics...

      </div>
    );
  }

  return (

    <div className="bg-black text-white min-h-screen p-6">

      <h1 className="text-4xl font-bold mb-8">

        Learning Analytics

      </h1>

      {/* Metrics */}
      <div className="grid grid-cols-3 gap-6 mb-8">

        <div className="bg-gray-900 p-6 rounded-xl">

          <h2 className="text-gray-400 mb-2">
            Total Topics
          </h2>

          <p className="text-3xl font-bold">

            {overview.total_topics}

          </p>

        </div>

        <div className="bg-gray-900 p-6 rounded-xl">

          <h2 className="text-gray-400 mb-2">
            Revision Needed
          </h2>

          <p className="text-3xl font-bold">

            {overview.revision_count}

          </p>

        </div>

        <div className="bg-gray-900 p-6 rounded-xl">

          <h2 className="text-gray-400 mb-2">
            Memory Health
          </h2>

          <p className="text-3xl font-bold">

            {Math.max(
              0,
              100 -
              overview.revision_count * 10
            )}%

          </p>

        </div>

      </div>

      {/* Revision Recommendations */}
      <div className="bg-gray-900 p-6 rounded-xl">

        <h2 className="text-2xl font-bold mb-4">

          Revision Queue

        </h2>

        {overview.revision_recommendations
          .length === 0 ? (

          <p className="text-gray-400">

            No revisions needed.

          </p>

        ) : (

          <div className="space-y-3">

            {overview
              .revision_recommendations
              .map(
                (
                  item: any,
                  idx: number
                ) => (

                  <div
                    key={idx}
                    className="bg-gray-800 p-4 rounded-lg"
                  >

                    <p className="font-semibold">

                      {item.topic}

                    </p>

                    <p className="text-sm text-gray-400">

                      {item.days_since_review}
                      {" "}
                      days since review

                    </p>

                  </div>

                )
              )}

          </div>

        )}

      </div>

    </div>
  );
}