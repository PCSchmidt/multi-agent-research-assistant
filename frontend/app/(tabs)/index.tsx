import { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, KeyboardAvoidingView, Platform } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MessageList } from '../../components/chat/MessageList';
import { PaperDetailsPanel } from '../../components/chat/PaperDetailsPanel';
import { AgentTimeline } from '../../components/timeline/AgentTimeline';
import { mockMessages } from '../../data/mockData';
import { Citation, Paper, Message, AgentStatus } from '../../types/research';

export default function ChatScreen() {
  // State for messages (using mock data for v0.3)
  const [messages, setMessages] = useState<Message[]>(mockMessages);
  const [inputValue, setInputValue] = useState('');

  // State for paper details panel
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const [isPaperPanelVisible, setIsPaperPanelVisible] = useState(false);

  // Get agent statuses from the last assistant message (if any)
  const lastAssistantMessage = [...messages].reverse().find((m) => m.role === 'assistant');
  const agentStatuses: AgentStatus[] = lastAssistantMessage?.agentStatuses || [];

  // Handle citation tap - find and display the paper
  const handleCitationPress = (citation: Citation) => {
    // Find the message containing this citation
    const messageWithCitation = messages.find(
      (msg) => msg.citations?.some((c) => c.number === citation.number)
    );

    if (messageWithCitation && messageWithCitation.papers) {
      // Find the paper by matching paperId
      const paper = messageWithCitation.papers.find((p) => p.id === citation.paperId);
      if (paper) {
        setSelectedPaper(paper);
        setIsPaperPanelVisible(true);
      }
    }
  };

  const handleClosePaperPanel = () => {
    setIsPaperPanelVisible(false);
    setTimeout(() => setSelectedPaper(null), 300); // Delay clearing to allow exit animation
  };

  const handleSubmit = () => {
    // TODO: v0.7+ - Wire to backend API
    // For now, just clear input (no actual submission)
    if (inputValue.trim()) {
      setInputValue('');
      // In future: create user message, trigger API call
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Research Assistant</Text>
        <Text style={styles.headerSubtitle}>Live academic search · Hybrid retrieval · Abstract synthesis</Text>
      </View>

      {/* Message list */}
      <View style={styles.contentContainer}>
        <View style={styles.messagesColumn}>
          <MessageList messages={messages} onCitationPress={handleCitationPress} />
        </View>

        {/* Agent Timeline (shown when there are agent statuses) */}
        {agentStatuses.length > 0 && (
          <View style={styles.timelineColumn}>
            <AgentTimeline statuses={agentStatuses} />
          </View>
        )}
      </View>

      {/* Query input */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="What would you like to research?"
            placeholderTextColor="#9B9388"
            multiline
            numberOfLines={2}
            value={inputValue}
            onChangeText={setInputValue}
            maxLength={500}
          />
          <TouchableOpacity
            style={[styles.submitButton, !inputValue.trim() && styles.submitButtonDisabled]}
            onPress={handleSubmit}
            disabled={!inputValue.trim()}
          >
            <Text style={styles.submitButtonText}>Submit Query</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>

      {/* Paper details panel */}
      <PaperDetailsPanel
        paper={selectedPaper}
        visible={isPaperPanelVisible}
        onClose={handleClosePaperPanel}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F3F0', // neutral-50
  },
  header: {
    padding: 20,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#D1CCC4', // neutral-200
  },
  contentContainer: {
    flex: 1,
    flexDirection: 'row',
    gap: 16,
    padding: 16,
    paddingTop: 0,
  },
  messagesColumn: {
    flex: 1,
  },
  timelineColumn: {
    width: 320,
    ...Platform.select({
      web: {
        display: 'flex',
      },
      default: {
        display: 'none', // Hide on mobile for now (v0.4 focuses on desktop layout)
      },
    }),
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '300',
    color: '#0F0D0A', // neutral-900
    marginBottom: 2,
  },
  headerSubtitle: {
    fontSize: 11,
    color: '#6B6358', // neutral-500
    fontStyle: 'italic',
  },
  inputContainer: {
    padding: 16,
    backgroundColor: '#FDFCFB', // surface
    borderTopWidth: 1,
    borderTopColor: '#D1CCC4', // neutral-200
    gap: 12,
  },
  input: {
    backgroundColor: '#F5F3F0', // neutral-50
    borderWidth: 1,
    borderColor: '#D1CCC4', // neutral-200
    borderBottomWidth: 2,
    borderBottomColor: '#9B9388', // neutral-300
    borderRadius: 2,
    padding: 16,
    fontSize: 15,
    color: '#0F0D0A', // neutral-900
    minHeight: 80,
    maxHeight: 120,
    textAlignVertical: 'top',
  },
  submitButton: {
    backgroundColor: '#D4A574', // primary-500
    borderWidth: 1,
    borderColor: 'rgba(107, 83, 52, 0.3)',
    borderRadius: 2,
    padding: 16,
    alignItems: 'center',
  },
  submitButtonDisabled: {
    backgroundColor: '#E8E5E0', // neutral-100
    borderColor: '#D1CCC4', // neutral-200
    opacity: 0.6,
  },
  submitButtonText: {
    fontSize: 13,
    fontWeight: '500',
    color: '#0F0D0A', // neutral-900
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
});
