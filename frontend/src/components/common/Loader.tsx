import React from 'react';
import './Loader.css';

interface LoaderProps {
    size?: 'sm' | 'md' | 'lg';
    text?: string;
}

export const Loader: React.FC<LoaderProps> = ({ size = 'md', text }) => {
    return (
        <div className="loader-container">
            <div className={`loader loader--${size}`} />
            {text && <p className="loader-text">{text}</p>}
        </div>
    );
};
