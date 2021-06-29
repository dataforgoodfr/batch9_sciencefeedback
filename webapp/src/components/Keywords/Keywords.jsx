import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { FiX } from "react-icons/fi";

import './keywords.css'



const Keywords = ({ data, onSubmit }) => {
    const { register, handleSubmit } = useForm();
    const [selected, setSelected] = useState(data);
    const [unselected, setUnselected] = useState([]);

    useEffect(() => {
        handleSubmit(onSubmit)()
        setSelected(data);
    }, [data, handleSubmit, setSelected]);

    const removeTag = (tag) => () => {
        setSelected(selected.filter((value) => value !== tag));
        handleSubmit(onSubmit)()
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="keywords">
            Here are the keywords we used
            <div className="select-zone">
                {selected.map((tag) => (
                    <div className="tag" key={tag}>
                        {tag}
                        <button onClick={removeTag(tag)}><FiX size={16} /></button>
                    </div>
                ))}
            </div>
        </form>
    );
};

export default Keywords;
