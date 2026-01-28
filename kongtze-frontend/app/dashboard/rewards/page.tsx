/**
 * Rewards Page
 * View points balance, history, and lucky draw
 */

'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { rewardsAPI } from '@/lib/api';

export default function RewardsPage() {
  const { token } = useAuth();
  const queryClient = useQueryClient();
  const [showLuckyDrawResult, setShowLuckyDrawResult] = useState(false);
  const [luckyDrawResult, setLuckyDrawResult] = useState<any>(null);

  const { data: balance, isLoading: balanceLoading } = useQuery({
    queryKey: ['rewards-balance'],
    queryFn: () => rewardsAPI.getBalance(token!),
    enabled: !!token,
  });

  const { data: history = [], isLoading: historyLoading } = useQuery({
    queryKey: ['rewards-history'],
    queryFn: () => rewardsAPI.getHistory(token!),
    enabled: !!token,
  });

  const luckyDrawMutation = useMutation({
    mutationFn: () => rewardsAPI.luckyDraw(token!),
    onSuccess: (result) => {
      setLuckyDrawResult(result);
      setShowLuckyDrawResult(true);
      queryClient.invalidateQueries({ queryKey: ['rewards-balance'] });
      queryClient.invalidateQueries({ queryKey: ['rewards-history'] });
    },
  });

  const handleLuckyDraw = () => {
    if (balance && balance.balance >= 100) {
      luckyDrawMutation.mutate();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Rewards</h1>
        <p className="text-gray-600 mt-1">Earn points and redeem rewards</p>
      </div>

      {/* Balance Card */}
      {balanceLoading ? (
        <div className="bg-white rounded-xl shadow-sm p-8 border">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="h-12 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      ) : (
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl shadow-lg p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium mb-2">Your Points Balance</p>
              <p className="text-5xl font-bold">{balance?.balance || 0}</p>
              <p className="text-blue-100 text-sm mt-2">
                Total earned: {balance?.total_earned || 0} points
              </p>
            </div>
            <div className="text-6xl">🏆</div>
          </div>
        </div>
      )}

      {/* Lucky Draw */}
      <div className="bg-white rounded-xl shadow-sm p-6 border">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Lucky Draw</h2>
            <p className="text-gray-600 text-sm">Spend 100 points for a chance to win prizes!</p>
          </div>
          <div className="text-4xl">🎰</div>
        </div>

        <button
          onClick={handleLuckyDraw}
          disabled={!balance || balance.balance < 100 || luckyDrawMutation.isPending}
          className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {luckyDrawMutation.isPending ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Drawing...
            </span>
          ) : balance && balance.balance < 100 ? (
            'Need 100 points'
          ) : (
            'Try Lucky Draw (100 points)'
          )}
        </button>
      </div>

      {/* Points History */}
      <div className="bg-white rounded-xl shadow-sm border">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold text-gray-900">Points History</h2>
        </div>

        {historyLoading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading history...</p>
          </div>
        ) : history.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-gray-600">No points history yet</p>
            <p className="text-sm text-gray-500 mt-2">
              Complete tests and homework to earn points!
            </p>
          </div>
        ) : (
          <div className="divide-y">
            {history.map((reward) => (
              <div key={reward.reward_id} className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      reward.points_change > 0 ? 'bg-green-100' : 'bg-red-100'
                    }`}
                  >
                    <span className="text-lg">
                      {reward.points_change > 0 ? '📈' : '📉'}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{reward.reason}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(reward.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div
                  className={`text-lg font-bold ${
                    reward.points_change > 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {reward.points_change > 0 ? '+' : ''}
                  {reward.points_change}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Lucky Draw Result Modal */}
      {showLuckyDrawResult && luckyDrawResult && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="text-6xl mb-4">
                {luckyDrawResult.won ? '🎉' : '😢'}
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {luckyDrawResult.won ? 'Congratulations!' : 'Better Luck Next Time!'}
              </h3>
              {luckyDrawResult.won && luckyDrawResult.gift && (
                <div className="bg-gradient-to-r from-yellow-100 to-orange-100 rounded-lg p-4 mb-4">
                  <p className="text-lg font-semibold text-gray-900">
                    {luckyDrawResult.gift.name}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {luckyDrawResult.gift.description}
                  </p>
                </div>
              )}
              <p className="text-gray-600 mb-6">
                {luckyDrawResult.won
                  ? 'You won a prize! Keep earning points for more chances.'
                  : 'Keep earning points and try again!'}
              </p>
              <button
                onClick={() => setShowLuckyDrawResult(false)}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

