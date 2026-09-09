import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// ---------- Courses ----------

export const getCourses = () => api.get("/courses").then((res) => res.data);

export const getCourse = (courseId) =>
  api.get(`/courses/${courseId}`).then((res) => res.data);

export const createCourse = (course) =>
  api.post("/courses", course).then((res) => res.data);

export const updateCourse = (courseId, course) =>
  api.put(`/courses/${courseId}`, course).then((res) => res.data);

export const deleteCourse = (courseId) => api.delete(`/courses/${courseId}`);

// ---------- Course Outcomes ----------

export const getOutcomes = (courseId) =>
  api.get(`/courses/${courseId}/outcomes`).then((res) => res.data);

export const createOutcome = (courseId, outcome) =>
  api.post(`/courses/${courseId}/outcomes`, outcome).then((res) => res.data);

export const updateOutcome = (coId, outcome) =>
  api.put(`/outcomes/${coId}`, outcome).then((res) => res.data);

export const deleteOutcome = (coId) => api.delete(`/outcomes/${coId}`);

// ---------- Students ----------

export const getStudents = (courseId) =>
  api.get(`/courses/${courseId}/students`).then((res) => res.data);

export const createStudent = (courseId, student) =>
  api.post(`/courses/${courseId}/students`, student).then((res) => res.data);

export const updateStudent = (studentId, student) =>
  api.put(`/students/${studentId}`, student).then((res) => res.data);

export const deleteStudent = (studentId) => api.delete(`/students/${studentId}`);

// ---------- Scores ----------

// Returns { students, outcomes, scores } in one call, so the frontend
// can build the full grid without a request per cell.
export const getScoreGrid = (courseId) =>
  api.get(`/courses/${courseId}/scores`).then((res) => res.data);

export const createScore = (score) =>
  api.post("/scores", score).then((res) => res.data);

export const updateScore = (scoreId, score) =>
  api.put(`/scores/${scoreId}`, score).then((res) => res.data);

// ---------- Attainment ----------

export const getAttainment = (coId, threshold) =>
  api
    .get(`/outcomes/${coId}/attainment`, { params: { threshold } })
    .then((res) => res.data);

export default api;
