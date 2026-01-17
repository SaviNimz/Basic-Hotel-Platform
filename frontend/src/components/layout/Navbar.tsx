import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../common/Button';
import './Navbar.css';

export const Navbar: React.FC = () => {
    const { isAuthenticated, logout } = useAuth();

    const handleLogout = () => {
        logout();
        window.location.href = '/login';
    };

    return (
        <nav className="navbar">
            <div className="navbar__container">
                <div className="navbar__brand">
                    <h1 className="navbar__title">Hotel Platform</h1>
                </div>
                {isAuthenticated && (
                    <div className="navbar__actions">
                        <Button variant="ghost" onClick={handleLogout}>
                            Logout
                        </Button>
                    </div>
                )}
            </div>
        </nav>
    );
};
