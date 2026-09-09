import CoursesPage from "./pages/CoursesPage";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 px-6 py-4">
        <h1 className="text-lg font-bold text-slate-900">
          Rubrix.ai — CO Attainment Calculator
        </h1>
        <p className="text-xs text-slate-500">
          Define course outcomes, record scores, and view attainment %.
        </p>
      </header>
      <main className="p-6 max-w-6xl mx-auto">
        <CoursesPage />
      </main>
    </div>
  );
}
