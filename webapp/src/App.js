import useKeywords from "./hooks/useKeywords";
import useResearchers from "./hooks/useResearchers";
import SearchBar from "./components/SearchBar";
import Keywords from "./components/Keywords";

import "./styles/App.css";
import ResearchersList from "./components/ResearchersList";

function App() {
  const { data: keywordsData, fetchKeywords } = useKeywords();
  const { data: researchersData, fetchResearchers } = useResearchers();

  const onSearchBarSubmit = (data) => {
    fetchKeywords(data);
  };

  const onKeywordsSubmit = (data) => {
    fetchResearchers(data);
  };

  return (
    <div className="App">
      <SearchBar onSubmit={onSearchBarSubmit} />

      {keywordsData && (
        <Keywords data={keywordsData} onSubmit={onKeywordsSubmit} />
      )}
      {researchersData && <ResearchersList data={researchersData} />}
    </div>
  );
}

export default App;
