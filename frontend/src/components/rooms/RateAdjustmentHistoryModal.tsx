import React from 'react';
import type { RateAdjustment, RoomType } from '../../api/types';
import { Modal } from '../common/Modal';
import { Loader } from '../common/Loader';
import './RateAdjustmentHistoryModal.css';

interface RateAdjustmentHistoryModalProps {
    isOpen: boolean;
    roomType: RoomType | null;
    adjustments: RateAdjustment[];
    loading: boolean;
    error: string;
    onClose: () => void;
}

export const RateAdjustmentHistoryModal: React.FC<RateAdjustmentHistoryModalProps> = ({
    isOpen,
    roomType,
    adjustments,
    loading,
    error,
    onClose,
}) => {
    return (
        <Modal isOpen={isOpen} onClose={onClose} title={`Rate History - ${roomType?.name ?? ''}`}>
            {loading ? (
                <Loader text="Loading rate history..." />
            ) : error ? (
                <div className="history-error">{error}</div>
            ) : adjustments.length === 0 ? (
                <div className="history-empty">No rate adjustments recorded yet.</div>
            ) : (
                <ul className="history-list">
                    {adjustments.map((adjustment) => (
                        <li key={adjustment.id} className="history-list__item">
                            <div className="history-list__row">
                                <span className="history-list__date">{adjustment.effective_date}</span>
                                <span className="history-list__amount">
                                    {adjustment.adjustment_amount >= 0 ? '+' : ''}
                                    {adjustment.adjustment_amount.toFixed(2)}
                                </span>
                            </div>
                            <p className="history-list__reason">{adjustment.reason}</p>
                        </li>
                    ))}
                </ul>
            )}
        </Modal>
    );
};
