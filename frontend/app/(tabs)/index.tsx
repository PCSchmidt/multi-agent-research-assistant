import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function ChatScreen() {
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Research Assistant</Text>
        <Text style={styles.headerSubtitle}>Multi-agent knowledge discovery</Text>
      </View>

      {/* Chat area (empty for now) */}
      <ScrollView style={styles.chatArea} contentContainerStyle={styles.chatContent}>
        <View style={styles.emptyState}>
          <Text style={styles.emptyStateTitle}>Begin Your Research</Text>
          <Text style={styles.emptyStateText}>
            Submit a query below and watch the multi-agent pipeline decompose, retrieve, critique, and synthesize knowledge.
          </Text>
        </View>
      </ScrollView>

      {/* Query input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="What would you like to research?"
          placeholderTextColor="#9B9388"
          multiline
          numberOfLines={2}
        />
        <TouchableOpacity style={styles.submitButton}>
          <Text style={styles.submitButtonText}>Submit Query</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F3F0', // neutral-50
  },
  header: {
    padding: 24,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#D1CCC4',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: '400',
    color: '#0F0D0A', // neutral-900
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#6B6358', // neutral-500
    fontStyle: 'italic',
  },
  chatArea: {
    flex: 1,
  },
  chatContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 24,
  },
  emptyState: {
    alignItems: 'center',
  },
  emptyStateTitle: {
    fontSize: 24,
    fontWeight: '400',
    color: '#0F0D0A',
    marginBottom: 16,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#6B6358',
    textAlign: 'center',
    lineHeight: 24,
    maxWidth: 400,
  },
  inputContainer: {
    padding: 16,
    backgroundColor: '#FDFCFB',
    borderTopWidth: 1,
    borderTopColor: '#D1CCC4',
    gap: 12,
  },
  input: {
    backgroundColor: '#F5F3F0',
    borderWidth: 1,
    borderColor: '#D1CCC4',
    borderBottomWidth: 2,
    borderBottomColor: '#9B9388',
    borderRadius: 2,
    padding: 16,
    fontSize: 16,
    color: '#0F0D0A',
    minHeight: 80,
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
  submitButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#0F0D0A',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
});
