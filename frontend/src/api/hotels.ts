import { apiClient } from './client';
import type { Hotel, HotelCreate, HotelUpdate, RoomType } from './types';


export const getHotels = async (skip = 0, limit = 100): Promise<Hotel[]> => {
    const response = await apiClient.get<Hotel[]>('/hotels/', {
        params: { skip, limit },
    });
    return response.data;
};


export const getHotel = async (hotelId: number): Promise<Hotel> => {
    const response = await apiClient.get<Hotel>(`/hotels/${hotelId}`);
    return response.data;
};


export const createHotel = async (hotel: HotelCreate): Promise<Hotel> => {
    const response = await apiClient.post<Hotel>('/hotels/', hotel);
    return response.data;
};

export const updateHotel = async (hotelId: number, hotel: HotelUpdate): Promise<Hotel> => {
    const response = await apiClient.put<Hotel>(`/hotels/${hotelId}`, hotel);
    return response.data;
};

export const deleteHotel = async (hotelId: number): Promise<Hotel> => {
    const response = await apiClient.delete<Hotel>(`/hotels/${hotelId}`);
    return response.data;
};


export const getRoomTypes = async (hotelId: number): Promise<RoomType[]> => {
    const response = await apiClient.get<RoomType[]>(`/hotels/${hotelId}/room-types/`);
    return response.data;
};
