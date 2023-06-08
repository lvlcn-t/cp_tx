import React from 'react';
import { useField } from 'formik';

interface FieldProps {
    name: string;
    label: string;
}

const Field: React.FC<FieldProps> = ({ name, label }) => {
    const [field, meta] = useField(name);

    return (
        <div>
            <label htmlFor={name}>{label}</label>
            <input id={name} type="text" {...field} />
            {meta.touched && meta.error ? <div>{meta.error}</div> : null}
        </div>
    );
};

export default Field;
