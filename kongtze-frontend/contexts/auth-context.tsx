/**
 * Authentication context and provider for Kongtze frontend
 * Manages user authentication state and tokens
 */

'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authAPI } from '@/lib/api';
import type { User, UserLogin } from '@/lib/types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: UserLogin) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = 'kongtze_token';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load token and user on mount
  useEffect(() => {
    const loadAuth = async () => {
      const savedToken = localStorage.getItem(TOKEN_KEY);

      if (savedToken) {
        try {
          const userData = await authAPI.getCurrentUser(savedToken);
          setToken(savedToken);
          setUser(userData);
        } catch (error) {
          // Token invalid, clear it
          localStorage.removeItem(TOKEN_KEY);
          setToken(null);
          setUser(null);
        }
      }

      setIsLoading(false);
    };

    loadAuth();
  }, []);

  const login = async (credentials: UserLogin) => {
    try {
      const response = await authAPI.login(credentials);
      const newToken = response.access_token;

      // Save token
      localStorage.setItem(TOKEN_KEY, newToken);
      setToken(newToken);

      // Fetch user data
      const userData = await authAPI.getCurrentUser(newToken);
      setUser(userData);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    if (token) {
      try {
        const userData = await authAPI.getCurrentUser(token);
        setUser(userData);
      } catch (error) {
        // Token invalid, logout
        logout();
      }
    }
  };

  const value: AuthContextType = {
    user,
    token,
    isLoading,
    isAuthenticated: !!user && !!token,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}
