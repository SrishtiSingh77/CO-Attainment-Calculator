import { useEffect, useState, useCallback } from "react";
import {
  getOutcomes,
  createOutcome,
  deleteOutcome,
  getStudents,
  createStudent,
  deleteStudent,
  getScoreGrid,
  createScore,
  updateScore,
} from "../api/client";
import OutcomeForm from "../components/OutcomeForm";
import StudentForm from "../components/StudentForm";
import ScoreGrid from "../components/ScoreGrid";
import AttainmentResults from "../components/AttainmentResults";

export default function CourseDetailPage({ course }) {
  const [outcomes, setOutcomes] = useState([]);
  const [students, setStudents] = useState([]);
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // Bumped every time a score is saved, so AttainmentResults refetches.
  const [scoresVersion, setScoresVersion] = useState(0);

  const loadAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [outcomesData, studentsData, gridData] = await Promise.all([
        getOutcomes(course.id),
        getStudents(course.id),
        getScoreGrid(course.id),
      ]);
      setOutcomes(outcomesData);
      setStudents(studentsData);
      setScores(gridData.scores);
    } catch {
      setError("Could not load course data. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, [course.id]);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const handleCreateOutcome = async (outcome) => {
    const created = await createOutcome(course.id, outcome);
    setOutcomes((prev) => [...prev, created]);
  };

  const handleDeleteOutcome = async (coId) => {
    await deleteOutcome(coId);
    setOutcomes((prev) => prev.filter((o) => o.id !== coId));
    setScores((prev) => prev.filter((s) => s.co_id !== coId));
  };

  const handleCreateStudent = async (student) => {
    const created = await createStudent(course.id, student);
    setStudents((prev) => [...prev, created]);
  };

  const handleDeleteStudent = async (studentId) => {
    await deleteStudent(studentId);
    setStudents((prev) => prev.filter((s) => s.id !== studentId));
    setScores((prev) => prev.filter((s) => s.student_id !== studentId));
  };

  // Upsert: create if no score exists for this student+CO yet, else update.
  const handleSaveScore = async (studentId, coId, marks, existingScore) => {
    let saved;
    if (existingScore) {
      saved = await updateScore(existingScore.id, { marks });
    } else {
      saved = await createScore({ student_id: studentId, co_id: coId, marks });
    }
    setScores((prev) => {
      const withoutThis = prev.filter(
        (s) => !(s.student_id === studentId && s.co_id === coId)
      );
      return [...withoutThis, saved];
    });
    setScoresVersion((v) => v + 1);
  };

  if (loading) {
    return <p className="text-sm text-slate-500">Loading course…</p>;
  }

  if (error) {
    return <p className="text-sm text-red-600">{error}</p>;
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-slate-800">
          {course.code} — {course.name}
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <OutcomeForm
          outcomes={outcomes}
          onCreate={handleCreateOutcome}
          onDelete={handleDeleteOutcome}
        />
        <StudentForm
          students={students}
          onCreate={handleCreateStudent}
          onDelete={handleDeleteStudent}
        />
      </div>

      <ScoreGrid
        students={students}
        outcomes={outcomes}
        scores={scores}
        onSaveScore={handleSaveScore}
      />

      <AttainmentResults outcomes={outcomes} scoresVersion={scoresVersion} />
    </div>
  );
}
