import { useState } from "react";

export default function ScoreGrid({ students, outcomes, scores, onSaveScore }) {
  // Track in-flight/just-saved cell state for lightweight feedback,
  // keyed by "studentId-coId".
  const [cellStatus, setCellStatus] = useState({});

  const scoreMap = new Map(scores.map((s) => [`${s.student_id}-${s.co_id}`, s]));

  const handleBlur = async (studentId, coId, rawValue, existingScore) => {
    const key = `${studentId}-${coId}`;

    if (rawValue === "") return; // don't save empty cells

    const marks = Number(rawValue);
    if (Number.isNaN(marks) || marks < 0 || marks > 100) {
      setCellStatus((prev) => ({ ...prev, [key]: "error" }));
      return;
    }

    // No-op if unchanged
    if (existingScore && existingScore.marks === marks) return;

    setCellStatus((prev) => ({ ...prev, [key]: "saving" }));
    try {
      await onSaveScore(studentId, coId, marks, existingScore);
      setCellStatus((prev) => ({ ...prev, [key]: "saved" }));
      setTimeout(() => {
        setCellStatus((prev) => ({ ...prev, [key]: undefined }));
      }, 1200);
    } catch {
      setCellStatus((prev) => ({ ...prev, [key]: "error" }));
    }
  };

  if (students.length === 0 || outcomes.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
        <h3 className="text-sm font-semibold text-slate-800 mb-2">Score Grid</h3>
        <p className="text-sm text-slate-500">
          Add at least one student and one course outcome to enter scores.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 overflow-x-auto">
      <h3 className="text-sm font-semibold text-slate-800 mb-3">
        Score Grid <span className="text-slate-400 font-normal">(marks out of 100)</span>
      </h3>
      <table className="min-w-full text-sm border-collapse">
        <thead>
          <tr>
            <th className="text-left font-medium text-slate-500 border-b border-slate-200 pb-2 pr-4">
              Student
            </th>
            {outcomes.map((co) => (
              <th
                key={co.id}
                className="text-center font-medium text-slate-500 border-b border-slate-200 pb-2 px-2 min-w-[80px]"
                title={co.description}
              >
                {co.code}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.id} className="border-b border-slate-100 last:border-0">
              <td className="py-2 pr-4 text-slate-700 whitespace-nowrap">
                {student.name}
                <span className="text-slate-400 text-xs ml-1">
                  ({student.roll_number})
                </span>
              </td>
              {outcomes.map((co) => {
                const key = `${student.id}-${co.id}`;
                const existing = scoreMap.get(key);
                const status = cellStatus[key];
                return (
                  <td key={co.id} className="px-2 py-1.5 text-center">
                    <input
                      type="number"
                      min="0"
                      max="100"
                      defaultValue={existing ? existing.marks : ""}
                      onBlur={(e) =>
                        handleBlur(student.id, co.id, e.target.value, existing)
                      }
                      className={`w-16 text-center text-sm border rounded-md px-1 py-1 focus:outline-none focus:ring-2 ${
                        status === "error"
                          ? "border-red-400 focus:ring-red-300"
                          : status === "saved"
                          ? "border-green-400 focus:ring-green-300"
                          : "border-slate-300 focus:ring-indigo-400"
                      }`}
                    />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-xs text-slate-400 mt-2">
        Enter a mark and click away from the cell to save. Green border = saved.
      </p>
    </div>
  );
}
