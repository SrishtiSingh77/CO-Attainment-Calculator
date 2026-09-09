import { useEffect, useState } from "react";
import { getAttainment } from "../api/client";

export default function AttainmentResults({ outcomes, scoresVersion }) {
  const [threshold, setThreshold] = useState(50);
  const [results, setResults] = useState({}); // co_id -> attainment result
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (outcomes.length === 0) {
      setResults({});
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.all(outcomes.map((co) => getAttainment(co.id, threshold)))
      .then((data) => {
        if (cancelled) return;
        const byId = {};
        data.forEach((r) => {
          byId[r.co_id] = r;
        });
        setResults(byId);
      })
      .catch(() => {
        if (!cancelled) setError("Could not load attainment results.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // scoresVersion changes whenever a score is saved elsewhere, so
    // results stay in sync without polling.
  }, [outcomes, threshold, scoresVersion]);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-800">Attainment Results</h3>
        <label className="flex items-center gap-2 text-sm text-slate-600">
          Threshold
          <input
            type="number"
            min="0"
            max="100"
            value={threshold}
            onChange={(e) => setThreshold(Number(e.target.value))}
            className="w-16 text-center border border-slate-300 rounded-md px-1 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />
        </label>
      </div>

      {loading && <p className="text-sm text-slate-500">Calculating…</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}

      {outcomes.length === 0 && !loading && (
        <p className="text-sm text-slate-500">Add course outcomes to see attainment.</p>
      )}

      {!loading && !error && outcomes.length > 0 && (
        <ul className="space-y-2">
          {outcomes.map((co) => {
            const result = results[co.id];
            if (!result) return null;
            const met = result.attainment_percentage >= threshold;
            return (
              <li
                key={co.id}
                className="flex items-center justify-between bg-slate-50 rounded-md px-3 py-2"
              >
                <div>
                  <span className="text-sm font-medium text-slate-800">{co.code}</span>
                  <span className="text-xs text-slate-500 ml-2">
                    {result.students_met}/{result.total_students} students met
                  </span>
                </div>
                <span
                  className={`text-sm font-semibold px-2 py-0.5 rounded ${
                    met ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"
                  }`}
                >
                  {result.attainment_percentage}%
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
