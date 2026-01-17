import React from 'react';
import { MainLayout } from '../components/layout/MainLayout';
import { Card } from '../components/common/Card';
import './NotFound.css';

export const NotFound: React.FC = () => {
    return (
        <MainLayout>
            <div className="not-found-container">
                <Card>
                    <div className="not-found-content">
                        <h1 className="not-found-title">404</h1>
                        <p className="not-found-text">Page not found</p>
                        <a href="/hotels" className="not-found-link">
                            Go to Hotels
                        </a>
                    </div>
                </Card>
            </div>
        </MainLayout>
    );
};
