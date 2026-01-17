import { apiClient } from './client';
import type { UserLogin, Token } from './types';

export const login = async (credentials: UserLogin): Promise<Token> => {

    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await apiClient.post<Token>('auth/token', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    return response.data;
};


export const logout = (): void => {
    localStorage.removeItem('access_token');
};
