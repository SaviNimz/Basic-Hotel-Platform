import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../common/Button';
import './Navbar.css';

export const Navbar: React.FC = () => {
    const { isAuthenticated, logout } = useAuth();
    const location = useLocation();

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
                        <div className="navbar__links">
                            <Link
                                to="/hotels"
                                className={
                                    location.pathname.startsWith('/hotels')
                                        ? 'navbar__link navbar__link--active'
                                        : 'navbar__link'
                                }
                            >
                                Hotels
                            </Link>
                            <Link
                                to="/rate-adjustments"
                                className={
                                    location.pathname === '/rate-adjustments'
                                        ? 'navbar__link navbar__link--active'
                                        : 'navbar__link'
                                }
                            >
                                Rate Adjustments
                            </Link>
                        </div>
                        <Button variant="ghost" onClick={handleLogout}>
                            Logout
                        </Button>
                    </div>
                )}
            </div>
        </nav>
    );
};
