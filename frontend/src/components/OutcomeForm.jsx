import { useState } from "react";

export default function OutcomeForm({ outcomes, onCreate, onDelete }) {
  const [code, setCode] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!code.trim() || !description.trim()) return;
    setSubmitting(true);
    try {
      await onCreate({ code: code.trim(), description: description.trim() });
      setCode("");
      setDescription("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
      <h3 className="text-sm font-semibold text-slate-800 mb-3">Course Outcomes</h3>

      {outcomes.length === 0 && (
        <p className="text-sm text-slate-500 mb-3">No outcomes defined yet.</p>
      )}

      <ul className="space-y-1.5 mb-3">
        {outcomes.map((co) => (
          <li
            key={co.id}
            className="flex items-start justify-between gap-2 text-sm bg-slate-50 rounded-md px-2.5 py-1.5"
          >
            <span>
              <span className="font-medium text-slate-800">{co.code}:</span>{" "}
              <span className="text-slate-600">{co.description}</span>
            </span>
            <button
              onClick={() => onDelete(co.id)}
              className="text-xs text-red-500 hover:text-red-700 shrink-0"
            >
              remove
            </button>
          </li>
        ))}
      </ul>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          placeholder="CO code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-24 text-sm border border-slate-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="flex-1 text-sm border border-slate-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          type="submit"
          disabled={submitting}
          className="text-sm bg-indigo-600 text-white rounded-md px-3 py-1.5 hover:bg-indigo-700 disabled:opacity-50 shrink-0"
        >
          Add
        </button>
      </form>
    </div>
  );
}
