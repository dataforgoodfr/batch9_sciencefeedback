import './researcher.css'
import ArticleList from "./ArticleList";

const Researcher = ({ name, data }) => {
    const nbArticle = data.articles.length;

    console.log(data)
    return (
        <div className="researcher" key={name}>
            <div className="researcher-info">
                <div className="researcher-name">{name}</div>
                <div className="researcher-tag">
                    <div className="researcher-tag-articles">
                        {nbArticle}{' '}{nbArticle > 1 ? 'articles' : 'article'}
                    </div>
                    <div className="researcher-tag-score">
                        Score:{' '}{data.score}
                    </div>
                </div>
                <div className="researcher-affiliation">
                    {data.affiliation.map(affiliation => <div>{affiliation}</div>)}
                </div>
            </div>

            <ArticleList articles={data.articles} name={name} />
        </div>
    );
}

export default Researcher;
