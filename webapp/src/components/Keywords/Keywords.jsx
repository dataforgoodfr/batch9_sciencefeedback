import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { FiX } from "react-icons/fi";

import './keywords.css'



const Keywords = ({ data, onSubmit }) => {
    const { register, handleSubmit } = useForm();
    const [selected, setSelected] = useState(data);

    useEffect(() => {
        handleSubmit(onSubmit)()
        setSelected(data);
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [data, handleSubmit, setSelected]);

    const removeTag = (tag) => () => {
        setSelected(selected.filter((value) => value !== tag));
        handleSubmit(onSubmit)()
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="keywords">
            { data.length > 0 && <>Here are the keywords we used</> }
            <div className="select-zone">
                {selected.map((tag) => (
                    <div className="tag" key={tag}>
                        {tag}
                        <button onClick={removeTag(tag)}><FiX size={16} /></button>
                    </div>
                ))}
                <input
                    defaultValue={selected}
                    type="hidden"
                    {...register("keywords", { required: true })}
                />
                <input
                    defaultValue={50}
                    type="hidden"
                    {...register("k", { required: true })}
                />
            </div>
        </form>
    );
};

export default Keywords;
