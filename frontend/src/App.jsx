import Dashboard from './components/home/Dashboard';
// import Auth from './components/auth/Auth'; // ← swap in when routing is wired up

/**
 * Top-level app shell.
 *
 * Until a router is added, App renders the Dashboard directly with
 * placeholder/empty props.  Replace these with real data from your
 * API layer once the backend is connected.
 */
function App() {
  // ─── Placeholder props (replace with API data) ──────────────────────────
  const dashboardProps = {
    username:     'Student',      // e.g. from auth context: user.displayName
    stats:        {},             // { workspaces, quizzes, accuracy, studyTime, questions }
    workspaces:   [],             // Array of workspace objects – slice(0,3) is applied inside
    quizzes:      [],             // Array of quiz objects    – slice(0,3) is applied inside
    streak:       { count: 0, daysCompleted: [false,false,false,false,false,false,false] },
    revisions:    [],             // Array of { id, subject, timing, timingColor }
    weekSummary:  { avgAccuracy: '--', studyTime: '--' },
    weeklyGraphImage: '',
  };
  // ────────────────────────────────────────────────────────────────────────

  return <Dashboard {...dashboardProps} />;
  // return <Auth />;
}

export default App;

