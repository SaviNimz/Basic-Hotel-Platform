import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHotels } from '../api/hotels';
import type { Hotel } from '../api/types';
import { MainLayout } from '../components/layout/MainLayout';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Loader } from '../components/common/Loader';
import './HotelList.css';

export const HotelList: React.FC = () => {
    const [hotels, setHotels] = useState<Hotel[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const navigate = useNavigate();

    useEffect(() => {
        const fetchHotels = async () => {
            try {
                const data = await getHotels();
                setHotels(data);
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to load hotels');
            } finally {
                setLoading(false);
            }
        };

        fetchHotels();
    }, []);

    if (loading) {
        return (
            <MainLayout>
                <Loader text="Loading hotels..." />
            </MainLayout>
        );
    }

    if (error) {
        return (
            <MainLayout>
                <div className="error-message">{error}</div>
            </MainLayout>
        );
    }

    return (
        <MainLayout>
            <div className="hotel-list-container">
                <div className="hotel-list-header">
                    <h1 className="hotel-list-title">Hotels</h1>
                    <p className="hotel-list-subtitle">Manage your hotel properties</p>
                </div>

                {hotels.length === 0 ? (
                    <Card>
                        <p className="empty-state">No hotels found. Create your first hotel to get started.</p>
                    </Card>
                ) : (
                    <div className="hotel-grid">
                        {hotels.map((hotel) => (
                            <Card key={hotel.id} hoverable>
                                <div className="hotel-card">
                                    <div className="hotel-card__content">
                                        <h3 className="hotel-card__title">{hotel.name}</h3>
                                        <p className="hotel-card__location">{hotel.location}</p>
                                        {hotel.is_active ? (
                                            <span className="hotel-card__badge hotel-card__badge--active">Active</span>
                                        ) : (
                                            <span className="hotel-card__badge hotel-card__badge--inactive">Inactive</span>
                                        )}
                                    </div>
                                    <div className="hotel-card__actions">
                                        <Button variant="primary" onClick={() => navigate(`/hotels/${hotel.id}`)}>
                                            View Details
                                        </Button>
                                    </div>
                                </div>
                            </Card>
                        ))}
                    </div>
                )}
            </div>
        </MainLayout>
    );
};
