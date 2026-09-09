import { useState } from "react";

export default function CourseList({
  courses,
  loading,
  error,
  selectedCourseId,
  onSelectCourse,
  onCreateCourse,
  onDeleteCourse,
}) {
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!code.trim() || !name.trim()) return;
    setSubmitting(true);
    try {
      await onCreateCourse({ code: code.trim(), name: name.trim() });
      setCode("");
      setName("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
      <h2 className="text-lg font-semibold text-slate-800 mb-3">Courses</h2>

      {loading && <p className="text-sm text-slate-500">Loading courses…</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}

      {!loading && !error && courses.length === 0 && (
        <p className="text-sm text-slate-500 mb-3">No courses yet. Add one below.</p>
      )}

      <ul className="space-y-1 mb-4">
        {courses.map((course) => (
          <li key={course.id}>
            <button
              onClick={() => onSelectCourse(course.id)}
              className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors flex justify-between items-center group ${
                selectedCourseId === course.id
                  ? "bg-indigo-600 text-white"
                  : "hover:bg-slate-100 text-slate-700"
              }`}
            >
              <span>
                <span className="font-medium">{course.code}</span> — {course.name}
              </span>
              <span
                onClick={(e) => {
                  e.stopPropagation();
                  if (confirm(`Delete ${course.code}? This removes all its data.`)) {
                    onDeleteCourse(course.id);
                  }
                }}
                className={`opacity-0 group-hover:opacity-100 text-xs px-2 py-0.5 rounded ${
                  selectedCourseId === course.id
                    ? "hover:bg-indigo-700"
                    : "hover:bg-red-100 text-red-600"
                }`}
              >
                delete
              </span>
            </button>
          </li>
        ))}
      </ul>

      <form onSubmit={handleSubmit} className="space-y-2 border-t border-slate-100 pt-3">
        <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">
          New course
        </p>
        <input
          type="text"
          placeholder="Course code (e.g. CS301)"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-full text-sm border border-slate-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <input
          type="text"
          placeholder="Course name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full text-sm border border-slate-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-indigo-600 text-white text-sm font-medium rounded-md py-1.5 hover:bg-indigo-700 disabled:opacity-50"
        >
          {submitting ? "Adding…" : "Add course"}
        </button>
      </form>
    </div>
  );
}
