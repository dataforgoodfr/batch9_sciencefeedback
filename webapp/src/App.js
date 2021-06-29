import useKeywords from "./hooks/useKeywords";
import useResearchers from "./hooks/useResearchers";
import SearchBar from "./components/SearchBar";
import Keywords from "./components/Keywords";

import ResearchersList from "./components/ResearchersList";
import Header from "./components/Header";

function App() {
    const { data: keywordsData, fetchKeywords } = useKeywords();
    const { data: researchersData, fetchResearchers } = useResearchers();

    const onSearchBarSubmit = async (data) => {
        fetchKeywords(data)
    };

    const onKeywordsSubmit = (data) => {
        fetchResearchers(data);
    };

    return (
        <div className="App">
            <Header />

            <div className="searchbar-keywords">
                <SearchBar onSubmit={onSearchBarSubmit} />

                {keywordsData && (
                    <Keywords data={keywordsData} onSubmit={onKeywordsSubmit} />
                )}
            </div>
            {researchersData && <ResearchersList data={researchersData} />}
        </div>
    );
}

export default App;
