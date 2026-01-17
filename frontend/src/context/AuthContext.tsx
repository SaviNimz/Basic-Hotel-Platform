import React, { createContext, useContext, useState, useEffect } from 'react';
import * as authApi from '../api/auth';
import type { UserLogin } from '../api/types';


// AUTH CONTEXT
// This Manages global authentication state

interface AuthContextType {
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: UserLogin) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    // Check for existing token on mount
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsAuthenticated(!!token);
        setIsLoading(false);
    }, []);

    const login = async (credentials: UserLogin) => {
        const tokenData = await authApi.login(credentials);
        localStorage.setItem('access_token', tokenData.access_token);
        setIsAuthenticated(true);
    };

    const logout = () => {
        authApi.logout();
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hook to use auth context
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
