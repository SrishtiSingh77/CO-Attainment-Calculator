import { useState } from "react";

export default function StudentForm({ students, onCreate, onDelete }) {
  const [name, setName] = useState("");
  const [rollNumber, setRollNumber] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !rollNumber.trim()) return;
    setSubmitting(true);
    try {
      await onCreate({ name: name.trim(), roll_number: rollNumber.trim() });
      setName("");
      setRollNumber("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
      <h3 className="text-sm font-semibold text-slate-800 mb-3">Students</h3>

      {students.length === 0 && (
        <p className="text-sm text-slate-500 mb-3">No students added yet.</p>
      )}

      <ul className="space-y-1.5 mb-3">
        {students.map((s) => (
          <li
            key={s.id}
            className="flex items-center justify-between text-sm bg-slate-50 rounded-md px-2.5 py-1.5"
          >
            <span>
              <span className="font-medium text-slate-800">{s.name}</span>{" "}
              <span className="text-slate-500">({s.roll_number})</span>
            </span>
            <button
              onClick={() => onDelete(s.id)}
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
          placeholder="Student name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="flex-1 text-sm border border-slate-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <input
          type="text"
          placeholder="Roll number"
          value={rollNumber}
          onChange={(e) => setRollNumber(e.target.value)}
          className="w-32 text-sm border border-slate-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
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
