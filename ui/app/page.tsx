"use client";

import { useEffect, useState } from "react";

// Define the shape of our Python data (from app/models/job.py)
interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  url: string;
  date_posted: string;
  source: string;
}

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/jobs")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Backend connection failed:", err);
      });
  }, []);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">📡 Job Radar</h1>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
            {jobs.length} Active Listings
          </span>
        </header>

        {loading ? (
          <p className="text-gray-500">Scanning frequencies...</p>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {jobs.map((job) => (
              <a
                key={job.id}
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block p-6 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <h2 className="text-xl font-semibold text-gray-800 line-clamp-2">
                    {job.title}
                  </h2>
                </div>
                <p className="text-blue-600 font-medium mb-4">{job.company}</p>

                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <span className="mr-2">📍</span>
                    {job.location || "Remote"}
                  </div>
                  <div className="flex items-center">
                    <span className="mr-2">📅</span>
                    {new Date(job.date_posted).toLocaleDateString()}
                  </div>
                  <div className="flex items-center">
                    <span className="mr-2">🔗</span>
                    <span className="capitalize">{job.source}</span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
