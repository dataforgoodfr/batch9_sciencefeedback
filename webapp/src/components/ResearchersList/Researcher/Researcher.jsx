import './researcher.css'
import ArticleList from "./ArticleList";

const Researcher = ({ name, data }) => {
    const { Affiliations: affiliations, Articles: articles, Score: score } = data
    const nbArticle = articles?.length;

    return (
        <div className="researcher">
            <div className="researcher-info">
                <div className="researcher-name">{name}</div>
                <div className="researcher-tag">
                    <div className="researcher-tag-articles">
                        {nbArticle}{' '}{nbArticle > 1 ? 'articles' : 'article'}
                    </div>
                    <div className="researcher-tag-score">
                        Score:{' '}{score}
                    </div>
                </div>
                <div className="researcher-affiliation">
                    {affiliations?.map(affiliation => <div>{affiliation}</div>)}
                </div>
            </div>

            <ArticleList articles={articles} name={name} />
        </div>
    );
}

export default Researcher;
