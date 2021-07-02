import './article.css'
import {useState} from "react";
import Modal from 'react-modal';

import { FiX } from "react-icons/fi";

const Article = ({ article, name }) => {
    const [open, setOpen] = useState(false);
    const formatDate = (date) => {
        let d = new Date(date);
        let ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
        let mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
        let da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
        return `${da} ${mo} ${ye}`
    }

    const openModal = () => {
        setOpen(true)
    }

    const closeModal = () => {
        setOpen(false)
    }

    const {
        Abstract: abstract,
        doi,
        Journal: journal,
        PublicationDate: publicationDate,
        Title: title
    } = article || {}

    return (
        <div className="article">
            <Modal
                isOpen={open}
                contentLabel="Minimal Modal Example"
                classname='test'
                style={{
                    overlay: {
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        backgroundColor: 'rgba(255, 255, 255, 0.75)'
                    },
                    content: {
                        position: 'absolute',
                        top: '40px',
                        left: '40px',
                        right: '40px',
                        bottom: '40px',
                        border: '1px solid #c6d9e8',
                        background: '#fff',
                        overflow: 'auto',
                        WebkitOverflowScrolling: 'touch',
                        borderRadius: '8px',
                        outline: 'none',
                        padding: '0'
                    }
                }}
            >
                <div className="article-modal-header">
                    {name} <button onClick={closeModal}><FiX size={24} /></button>
                </div>
                <div className="article-modal-content">
                    <a className="article-title" rel="noreferrer" target="_blank" href={doi}>{title}</a>
                    <div className="article-date">{formatDate(publicationDate)}
                    </div>
                    <div className="article-newspaper">{journal}</div>

                    <div className="article-abstract">{abstract}</div>
                </div>
            </Modal>

            <a className="article-title" rel="noreferrer" target="_blank" href={doi}>{title}</a>
            <div className="article-date">{formatDate(publicationDate)}
                <button className="article-show-abstract" onClick={openModal}>Show Abstract</button>
            </div>
            <div className="article-newspaper">{journal}</div>
        </div>

    );
}

export default Article;
