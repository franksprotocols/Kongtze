/**
 * Test Results Page
 * Shows score and detailed review with correct answers
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { testsAPI } from '@/lib/api';
import Link from 'next/link';

export default function TestResultPage({ params }: { params: { resultId: string } }) {
  const { token } = useAuth();
  const resultId = parseInt(params.resultId);

  const { data: result, isLoading } = useQuery({
    queryKey: ['test-result', resultId],
    queryFn: () => testsAPI.getResult(resultId, token!),
    enabled: !!token,
  });

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading results...</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Results not found</p>
      </div>
    );
  }

  const percentage = result.percentage;
  const passed = percentage >= 70;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Results Summary */}
      <div className={`rounded-xl shadow-lg p-8 text-white ${passed ? 'bg-gradient-to-r from-green-500 to-green-600' : 'bg-gradient-to-r from-orange-500 to-orange-600'}`}>
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">
            {passed ? '🎉 Great Job!' : '💪 Keep Practicing!'}
          </h1>

          <div className="bg-white bg-opacity-20 rounded-lg p-6 mb-6">
            <div className="text-6xl font-bold mb-2">{percentage.toFixed(0)}%</div>
            <div className="text-xl">
              {result.score} out of {result.total_score} correct
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-sm opacity-90">Time Taken</p>
              <p className="text-2xl font-semibold">
                {Math.floor(result.time_taken_seconds / 60)}:{(result.time_taken_seconds % 60).toString().padStart(2, '0')}
              </p>
            </div>
            <div>
              <p className="text-sm opacity-90">Points Earned</p>
              <p className="text-2xl font-semibold">+{result.reward_points}</p>
            </div>
            <div>
              <p className="text-sm opacity-90">Accuracy</p>
              <p className="text-2xl font-semibold">{percentage.toFixed(1)}%</p>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <Link
          href="/dashboard/tests/new"
          className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-center"
        >
          Generate New Test
        </Link>
        <Link
          href="/dashboard/tests"
          className="flex-1 px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium text-center text-gray-700"
        >
          Back to Tests
        </Link>
      </div>

      {/* Detailed Review */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Detailed Review</h2>

        <div className="space-y-6">
          {result.questions.map((question, index) => {
            const userAnswer = result.answers[question.question_id];
            const isCorrect = userAnswer === question.correct_answer;

            return (
              <div
                key={question.question_id}
                className={`p-6 rounded-lg border-2 ${
                  isCorrect
                    ? 'border-green-200 bg-green-50'
                    : 'border-red-200 bg-red-50'
                }`}
              >
                {/* Question Number and Status */}
                <div className="flex items-center justify-between mb-4">
                  <span className="font-semibold text-gray-900">Question {index + 1}</span>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      isCorrect
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {isCorrect ? '✓ Correct' : '✗ Incorrect'}
                  </span>
                </div>

                {/* Question Text */}
                <p className="text-gray-900 font-medium mb-4">{question.question_text}</p>

                {/* Options */}
                <div className="space-y-2">
                  {Object.entries(question.options).map(([key, value]) => {
                    const isUserAnswer = userAnswer === key;
                    const isCorrectAnswer = key === question.correct_answer;

                    let className = 'p-3 rounded-lg border-2 ';
                    if (isCorrectAnswer) {
                      className += 'border-green-500 bg-green-100';
                    } else if (isUserAnswer && !isCorrect) {
                      className += 'border-red-500 bg-red-100';
                    } else {
                      className += 'border-gray-200 bg-white';
                    }

                    return (
                      <div key={key} className={className}>
                        <div className="flex items-start gap-2">
                          <span className="font-semibold">{key}.</span>
                          <span className="flex-1">{value}</span>
                          {isCorrectAnswer && (
                            <span className="text-green-600 font-semibold">✓ Correct Answer</span>
                          )}
                          {isUserAnswer && !isCorrect && (
                            <span className="text-red-600 font-semibold">Your Answer</span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Explanation (if available) */}
                {!isCorrect && (
                  <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <p className="text-sm font-medium text-blue-900 mb-1">💡 Explanation:</p>
                    <p className="text-sm text-blue-800">
                      The correct answer is <strong>{question.correct_answer}</strong>.
                      Review this concept in your notes and try similar practice questions.
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Performance Tips */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-3">📚 Study Tips:</h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>✓ Review the questions you got wrong</li>
          <li>✓ Practice more questions at the same difficulty level</li>
          {percentage < 70 && <li>✓ Consider revisiting the class notes for this topic</li>}
          {percentage >= 90 && <li>✓ Great work! Try a higher difficulty level next time</li>}
          <li>✓ Keep taking regular tests to track your progress</li>
        </ul>
      </div>
    </div>
  );
}
