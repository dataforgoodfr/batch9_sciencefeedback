import './articleList.css'
import {useState} from "react";
import Article from "./Article";

const ArticleList = ({ name, articles }) => {
    const [isCollapsed, setIsCollapsed] = useState(true);

    return (
        <>
            <div
                className={`article-list collapse-content ${isCollapsed ? 'collapsed' : 'expanded'}`}
                aria-expanded={isCollapsed}
            >
                Articles
                {articles.map(article =>
                    <Article article={article} name={name} />
                )}
            </div>

            <button
                className="collapse-button"
                onClick={() => setIsCollapsed(!isCollapsed)}
            >
                {isCollapsed ? 'See more' : 'See less'}
            </button>
        </>
    );
}

export default ArticleList;
