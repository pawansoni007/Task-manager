import { useTasks } from './hooks/useTasks';
import { TaskForm } from './components/TaskForm';
import { TaskList } from './components/TaskList';
import { FilterBar } from './components/FilterBar';
import { SearchBar } from './components/SearchBar';
import { TaskStats } from './components/TaskStats';

// Top-level composition: the hook owns all data/state, components render it.
export function App() {
  const {
    tasks,
    stats,
    filter,
    search,
    loading,
    error,
    setFilter,
    setSearch,
    createTask,
    updateTask,
    removeTask,
  } = useTasks();

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">Mini Task Tracker</h1>
        <p className="app__subtitle">A simple, focused way to track your tasks.</p>
      </header>

      <main className="app__main">
        <TaskForm onCreate={createTask} />

        <section className="app__controls">
          <SearchBar value={search} onChange={setSearch} />
          <FilterBar value={filter} onChange={setFilter} />
        </section>

        <TaskStats stats={stats} />

        {error && <p className="app__error">{error}</p>}

        <TaskList
          tasks={tasks}
          loading={loading}
          filter={filter}
          search={search}
          onUpdate={updateTask}
          onDelete={removeTask}
        />
      </main>
    </div>
  );
}
