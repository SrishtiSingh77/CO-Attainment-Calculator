import { useEffect, useState } from "react";
import { getCourses, createCourse, deleteCourse } from "../api/client";
import CourseList from "../components/CourseList";
import CourseDetailPage from "./CourseDetailPage";

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCourseId, setSelectedCourseId] = useState(null);

  useEffect(() => {
    getCourses()
      .then((data) => {
        setCourses(data);
        if (data.length > 0) setSelectedCourseId(data[0].id);
      })
      .catch(() => setError("Could not load courses. Is the backend running?"))
      .finally(() => setLoading(false));
  }, []);

  const handleCreateCourse = async (course) => {
    const created = await createCourse(course);
    setCourses((prev) => [...prev, created]);
    setSelectedCourseId(created.id);
  };

  const handleDeleteCourse = async (courseId) => {
    await deleteCourse(courseId);
    setCourses((prev) => prev.filter((c) => c.id !== courseId));
    setSelectedCourseId((current) => (current === courseId ? null : current));
  };

  const selectedCourse = courses.find((c) => c.id === selectedCourseId);

  return (
    <div className="grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4">
      <CourseList
        courses={courses}
        loading={loading}
        error={error}
        selectedCourseId={selectedCourseId}
        onSelectCourse={setSelectedCourseId}
        onCreateCourse={handleCreateCourse}
        onDeleteCourse={handleDeleteCourse}
      />

      <div>
        {selectedCourse ? (
          <CourseDetailPage key={selectedCourse.id} course={selectedCourse} />
        ) : (
          !loading && (
            <p className="text-sm text-slate-500">
              Select a course on the left, or add a new one to get started.
            </p>
          )
        )}
      </div>
    </div>
  );
}
