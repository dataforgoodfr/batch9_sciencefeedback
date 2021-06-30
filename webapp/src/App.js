import useKeywords from "./hooks/useKeywords";
import useResearchers from "./hooks/useResearchers";
import SearchBar from "./components/SearchBar";
import Keywords from "./components/Keywords";

import ResearchersList from "./components/ResearchersList";
import Header from "./components/Header";

function App() {
    const { data: keywordsData, error: keywordsError, fetchKeywords, isLoading: isLoadingKeywords } = useKeywords();
    const { data: researchersData, error: researchersError, fetchResearchers, isLoading: isLoadingResearchers } = useResearchers();

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
                { isLoadingKeywords && !keywordsError && <div className="text-center">Loading keywords...</div> }
                { keywordsError && <div className="text-center">Error loading keywords</div> }
                { keywordsData && (
                    <Keywords data={keywordsData} onSubmit={onKeywordsSubmit} />
                ) }
            </div>

            { isLoadingResearchers && !researchersError && <div className="text-center">Loading researchers...</div> }
            { researchersError && <div className="text-center">Error loading researchers</div> }
            { keywordsData && researchersData && <ResearchersList data={researchersData} /> }

        </div>
    );
}

export default App;
