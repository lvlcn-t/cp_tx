import React from 'react';
import { useField } from 'formik';

interface DropdownProps {
    name: string;
    label: string;
    options: { value: string; label: string }[];
}

const Dropdown: React.FC<DropdownProps> = ({ name, label, options }) => {
    const [field, meta] = useField(name);

    return (
        <div>
            <label htmlFor={name}>{label}</label>
            <select id={name} {...field}>
                {options.map((option, index) => (
                    <option key={index} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
            {meta.touched && meta.error ? <div>{meta.error}</div> : null}
        </div>
    );
};

export default Dropdown;