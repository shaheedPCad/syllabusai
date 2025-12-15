'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { joinCourse } from '@/services/courses';
import { UserPlus, Loader2 } from 'lucide-react';

interface JoinCourseProps {
  onCourseJoined: () => void;
}

export function JoinCourse({ onCourseJoined }: JoinCourseProps) {
  const [joinCode, setJoinCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleJoin = async () => {
    if (!joinCode.trim()) {
      setError('Please enter a join code');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await joinCourse(joinCode.trim());

      // Success
      setJoinCode('');
      onCourseJoined();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      const errorMessage = error.response?.data?.detail || 'Failed to join course';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleJoin();
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <div className="flex gap-2">
        <Input
          placeholder="Enter join code (e.g., ABC123)"
          value={joinCode}
          onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
          onKeyPress={handleKeyPress}
          disabled={loading}
          className="max-w-[200px]"
        />
        <Button onClick={handleJoin} disabled={loading || !joinCode.trim()}>
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Joining...
            </>
          ) : (
            <>
              <UserPlus className="mr-2 h-4 w-4" />
              Join Course
            </>
          )}
        </Button>
      </div>
      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}
    </div>
  );
}
