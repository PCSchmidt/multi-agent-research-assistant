// StreamingMessage - Displays an assistant message with streaming animation and citations

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Message, Citation, Paper } from '../../types/research';
import { CitationRenderer } from './CitationRenderer';

interface StreamingMessageProps {
  message: Message;
  onCitationPress: (citation: Citation) => void;
}

export function StreamingMessage({ message, onCitationPress }: StreamingMessageProps) {
  const isUser = message.role === 'user';

  // Parse content and inject citation components
  const renderContentWithCitations = () => {
    if (isUser || !message.citations || message.citations.length === 0) {
      return <Text style={styles.contentText}>{message.content}</Text>;
    }

    // Split content by citation markers [1], [2], etc.
    const citationPattern = /\[(\d+)\]/g;
    const parts = message.content.split(citationPattern);
    const elements: React.ReactNode[] = [];

    for (let i = 0; i < parts.length; i++) {
      if (i % 2 === 0) {
        // Regular text
        if (parts[i]) {
          elements.push(
            <Text key={`text-${i}`} style={styles.contentText}>
              {parts[i]}
            </Text>
          );
        }
      } else {
        // Citation number
        const citationNumber = parseInt(parts[i], 10);
        const citation = message.citations.find((c) => c.number === citationNumber);
        if (citation) {
          elements.push(
            <CitationRenderer
              key={`citation-${i}`}
              citation={citation}
              onPress={onCitationPress}
            />
          );
        }
      }
    }

    return <Text>{elements}</Text>;
  };

  // Format timestamp
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
  };

  return (
    <View style={[styles.messageContainer, isUser && styles.userMessageContainer]}>
      <View style={[styles.messageBubble, isUser && styles.userBubble]}>
        {/* Role label */}
        <Text style={[styles.roleLabel, isUser && styles.userRoleLabel]}>
          {isUser ? 'You' : 'Research Assistant'}
        </Text>

        {/* Content with citations */}
        <View style={styles.contentContainer}>{renderContentWithCitations()}</View>

        {/* Streaming indicator */}
        {message.isStreaming && (
          <View style={styles.streamingIndicator}>
            <View style={[styles.streamingDot, styles.streamingDot1]} />
            <View style={[styles.streamingDot, styles.streamingDot2]} />
            <View style={[styles.streamingDot, styles.streamingDot3]} />
          </View>
        )}

        {/* Eval scores badge */}
        {!isUser && message.evalScores && message.evalScores.status === 'completed' && (
          <View style={styles.evalBadge}>
            <Text style={styles.evalBadgeLabel}>Quality Scores</Text>
            <View style={styles.evalScoresRow}>
              {message.evalScores.faithfulness !== undefined && (
                <View style={styles.evalScore}>
                  <Text style={styles.evalScoreValue}>
                    {(message.evalScores.faithfulness * 100).toFixed(0)}%
                  </Text>
                  <Text style={styles.evalScoreLabel}>Faithfulness</Text>
                </View>
              )}
              {message.evalScores.answerRelevancy !== undefined && (
                <View style={styles.evalScore}>
                  <Text style={styles.evalScoreValue}>
                    {(message.evalScores.answerRelevancy * 100).toFixed(0)}%
                  </Text>
                  <Text style={styles.evalScoreLabel}>Relevancy</Text>
                </View>
              )}
              {message.evalScores.citationAccuracy !== undefined && (
                <View style={styles.evalScore}>
                  <Text style={styles.evalScoreValue}>
                    {(message.evalScores.citationAccuracy * 100).toFixed(0)}%
                  </Text>
                  <Text style={styles.evalScoreLabel}>Citation Acc.</Text>
                </View>
              )}
            </View>
          </View>
        )}

        {/* Timestamp */}
        <Text style={styles.timestamp}>{formatTime(message.timestamp)}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  messageContainer: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    alignItems: 'flex-start',
  },
  userMessageContainer: {
    alignItems: 'flex-end',
  },
  messageBubble: {
    maxWidth: '85%',
    backgroundColor: '#FDFCFB', // surface
    borderWidth: 1,
    borderColor: '#D1CCC4', // neutral-200
    borderBottomWidth: 2,
    borderBottomColor: '#9B9388', // neutral-300
    borderRadius: 4,
    padding: 16,
    gap: 12,
  },
  userBubble: {
    backgroundColor: 'rgba(212, 165, 116, 0.08)', // primary-500 tint
    borderColor: '#D4A574', // primary-500
    borderBottomColor: '#B8935F', // primary-600
  },
  roleLabel: {
    fontSize: 11,
    fontWeight: '600',
    color: '#6B6358', // neutral-500
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  userRoleLabel: {
    color: '#B8935F', // primary-600
  },
  contentContainer: {
    gap: 4,
  },
  contentText: {
    fontSize: 15,
    color: '#0F0D0A', // neutral-900
    lineHeight: 24,
  },
  streamingIndicator: {
    flexDirection: 'row',
    gap: 6,
    paddingVertical: 4,
  },
  streamingDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#D4A574', // primary-500
  },
  streamingDot1: {
    opacity: 0.4,
  },
  streamingDot2: {
    opacity: 0.7,
  },
  streamingDot3: {
    opacity: 1,
  },
  evalBadge: {
    marginTop: 8,
    padding: 12,
    backgroundColor: 'rgba(124, 152, 133, 0.08)', // success-500 tint
    borderWidth: 1,
    borderColor: '#7C9885', // success-500
    borderRadius: 4,
    gap: 8,
  },
  evalBadgeLabel: {
    fontSize: 10,
    fontWeight: '600',
    color: '#5A7A65', // success-600
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  evalScoresRow: {
    flexDirection: 'row',
    gap: 16,
  },
  evalScore: {
    gap: 2,
  },
  evalScoreValue: {
    fontSize: 16,
    fontWeight: '500',
    color: '#0F0D0A', // neutral-900
  },
  evalScoreLabel: {
    fontSize: 10,
    color: '#6B6358', // neutral-500
  },
  timestamp: {
    fontSize: 11,
    color: '#9B9388', // neutral-300
    fontStyle: 'italic',
  },
});
