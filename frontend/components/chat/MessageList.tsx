// MessageList - Scrollable list of chat messages with empty state

import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, ListRenderItem } from 'react-native';
import { Message, Citation } from '../../types/research';
import { StreamingMessage } from './StreamingMessage';

interface MessageListProps {
  messages: Message[];
  onCitationPress: (citation: Citation) => void;
}

export function MessageList({ messages, onCitationPress }: MessageListProps) {
  const flatListRef = useRef<FlatList>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messages.length > 0 && flatListRef.current) {
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [messages.length]);

  const renderMessage: ListRenderItem<Message> = ({ item }) => (
    <StreamingMessage message={item} onCitationPress={onCitationPress} />
  );

  const renderEmptyState = () => (
    <View style={styles.emptyStateContainer}>
      <View style={styles.emptyState}>
        <Text style={styles.emptyStateIcon}>🔬</Text>
        <Text style={styles.emptyStateTitle}>Begin Your Research</Text>
        <Text style={styles.emptyStateText}>
          Submit a query below. The research assistant will search live academic databases
          (Semantic Scholar, arXiv) and local canonical works to synthesize a comprehensive answer
          with proper citations.
        </Text>
        <View style={styles.exampleQueriesContainer}>
          <Text style={styles.exampleQueriesLabel}>Example queries:</Text>
          <Text style={styles.exampleQuery}>
            • What are recent advances in sparse attention mechanisms?
          </Text>
          <Text style={styles.exampleQuery}>
            • Survey papers on vision transformers from 2022-2024
          </Text>
          <Text style={styles.exampleQuery}>
            • What are the main approaches to few-shot learning in NLP?
          </Text>
        </View>
      </View>
    </View>
  );

  return (
    <FlatList
      ref={flatListRef}
      data={messages}
      renderItem={renderMessage}
      keyExtractor={(item) => item.id}
      contentContainerStyle={[
        styles.listContent,
        messages.length === 0 && styles.emptyListContent,
      ]}
      ListEmptyComponent={renderEmptyState}
      showsVerticalScrollIndicator={true}
      maintainVisibleContentPosition={
        messages.length > 0
          ? {
              minIndexForVisible: 0,
              autoscrollToTopThreshold: 10,
            }
          : undefined
      }
    />
  );
}

const styles = StyleSheet.create({
  listContent: {
    paddingVertical: 16,
  },
  emptyListContent: {
    flexGrow: 1,
  },
  emptyStateContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  emptyState: {
    maxWidth: 500,
    alignItems: 'center',
    gap: 16,
  },
  emptyStateIcon: {
    fontSize: 48,
    marginBottom: 8,
  },
  emptyStateTitle: {
    fontSize: 28,
    fontWeight: '300',
    color: '#0F0D0A', // neutral-900
    textAlign: 'center',
  },
  emptyStateText: {
    fontSize: 15,
    color: '#6B6358', // neutral-500
    textAlign: 'center',
    lineHeight: 24,
  },
  exampleQueriesContainer: {
    marginTop: 16,
    width: '100%',
    padding: 16,
    backgroundColor: 'rgba(212, 165, 116, 0.06)', // primary-500 subtle tint
    borderWidth: 1,
    borderColor: '#D1CCC4', // neutral-200
    borderRadius: 4,
    gap: 8,
  },
  exampleQueriesLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#B8935F', // primary-600
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  exampleQuery: {
    fontSize: 14,
    color: '#3D3832', // neutral-700
    lineHeight: 20,
    fontStyle: 'italic',
  },
});
