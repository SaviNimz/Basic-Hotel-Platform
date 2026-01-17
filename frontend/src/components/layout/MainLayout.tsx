import React from 'react';
import { Navbar } from './Navbar';
import './MainLayout.css';

interface MainLayoutProps {
    children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
    return (
        <div className="main-layout">
            <Navbar />
            <main className="main-layout__content">{children}</main>
        </div>
    );
};
