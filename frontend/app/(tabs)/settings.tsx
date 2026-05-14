import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput, ActivityIndicator, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { saveAPIKey, listAPIKeys, deleteAPIKey, testAPIKey, type Provider, type APIKeyResponse } from '../../lib/apiKeys';

interface ProviderState {
  value: string;
  saved: boolean;
  loading: boolean;
  testing: boolean;
  showKey: boolean;
}

export default function SettingsScreen() {
  const [anthropic, setAnthropic] = useState<ProviderState>({ value: '', saved: false, loading: false, testing: false, showKey: false });
  const [openai, setOpenai] = useState<ProviderState>({ value: '', saved: false, loading: false, testing: false, showKey: false });
  const [openrouter, setOpenrouter] = useState<ProviderState>({ value: '', saved: false, loading: false, testing: false, showKey: false });
  const [loadingKeys, setLoadingKeys] = useState(true);

  // Load existing keys on mount
  useEffect(() => {
    loadSavedKeys();
  }, []);

  async function loadSavedKeys() {
    try {
      const keys = await listAPIKeys();
      const providers: { [key: string]: boolean } = {};
      keys.forEach((key: APIKeyResponse) => {
        providers[key.provider] = true;
      });

      setAnthropic(prev => ({ ...prev, saved: providers['anthropic'] || false }));
      setOpenai(prev => ({ ...prev, saved: providers['openai'] || false }));
      setOpenrouter(prev => ({ ...prev, saved: providers['openrouter'] || false }));
    } catch (error) {
      console.error('Failed to load API keys:', error);
    } finally {
      setLoadingKeys(false);
    }
  }

  async function handleSave(provider: Provider, value: string, setState: React.Dispatch<React.SetStateAction<ProviderState>>) {
    if (!value.trim()) {
      Alert.alert('Error', 'Please enter an API key');
      return;
    }

    setState(prev => ({ ...prev, loading: true }));
    try {
      await saveAPIKey(provider, value.trim());
      setState(prev => ({ ...prev, saved: true, loading: false, value: '' }));
      Alert.alert('Success', `${provider.charAt(0).toUpperCase() + provider.slice(1)} API key saved successfully`);
    } catch (error) {
      setState(prev => ({ ...prev, loading: false }));
      Alert.alert('Error', error instanceof Error ? error.message : 'Failed to save API key');
    }
  }

  async function handleTest(provider: Provider, setState: React.Dispatch<React.SetStateAction<ProviderState>>) {
    setState(prev => ({ ...prev, testing: true }));
    try {
      const result = await testAPIKey(provider);
      setState(prev => ({ ...prev, testing: false }));

      if (result.success) {
        Alert.alert('Success', `${provider.charAt(0).toUpperCase() + provider.slice(1)} API key is valid`);
      } else {
        Alert.alert('Error', result.error || 'API key test failed');
      }
    } catch (error) {
      setState(prev => ({ ...prev, testing: false }));
      Alert.alert('Error', error instanceof Error ? error.message : 'Failed to test API key');
    }
  }

  async function handleDelete(provider: Provider, setState: React.Dispatch<React.SetStateAction<ProviderState>>) {
    Alert.alert(
      'Delete API Key',
      `Are you sure you want to delete your ${provider.charAt(0).toUpperCase() + provider.slice(1)} API key?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            setState(prev => ({ ...prev, loading: true }));
            try {
              await deleteAPIKey(provider);
              setState(prev => ({ ...prev, saved: false, loading: false, value: '' }));
              Alert.alert('Success', 'API key deleted successfully');
            } catch (error) {
              setState(prev => ({ ...prev, loading: false }));
              Alert.alert('Error', error instanceof Error ? error.message : 'Failed to delete API key');
            }
          },
        },
      ]
    );
  }

  function renderProviderSection(
    title: string,
    provider: Provider,
    state: ProviderState,
    setState: React.Dispatch<React.SetStateAction<ProviderState>>
  ) {
    return (
      <View style={styles.providerSection}>
        <Text style={styles.providerTitle}>{title}</Text>

        {state.saved ? (
          <View>
            <Text style={styles.savedText}>✓ API key configured</Text>
            <View style={styles.buttonRow}>
              <TouchableOpacity
                style={[styles.button, styles.testButton]}
                onPress={() => handleTest(provider, setState)}
                disabled={state.testing}
              >
                {state.testing ? (
                  <ActivityIndicator size="small" color="#D4A574" />
                ) : (
                  <Text style={styles.buttonText}>Test Connection</Text>
                )}
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, styles.deleteButton]}
                onPress={() => handleDelete(provider, setState)}
                disabled={state.loading}
              >
                <Text style={styles.deleteButtonText}>Delete</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <View>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder={`Enter ${title} API key`}
                placeholderTextColor="#9B9388"
                value={state.value}
                onChangeText={(text) => setState(prev => ({ ...prev, value: text }))}
                secureTextEntry={!state.showKey}
                autoCapitalize="none"
                autoCorrect={false}
              />
              <TouchableOpacity
                style={styles.showButton}
                onPress={() => setState(prev => ({ ...prev, showKey: !prev.showKey }))}
              >
                <Text style={styles.showButtonText}>{state.showKey ? 'Hide' : 'Show'}</Text>
              </TouchableOpacity>
            </View>
            <TouchableOpacity
              style={[styles.button, styles.saveButton]}
              onPress={() => handleSave(provider, state.value, setState)}
              disabled={state.loading || !state.value.trim()}
            >
              {state.loading ? (
                <ActivityIndicator size="small" color="#FDFCFB" />
              ) : (
                <Text style={styles.saveButtonText}>Save API Key</Text>
              )}
            </TouchableOpacity>
          </View>
        )}
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Settings</Text>
        <Text style={styles.headerSubtitle}>Configure your research environment</Text>
      </View>

      <ScrollView style={styles.content}>
        {/* Account section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>
          <View style={styles.card}>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Email</Text>
              <Text style={styles.settingValue}>user@example.com</Text>
            </View>
          </View>
        </View>

        {/* API Keys section (BYOK) */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>API Keys (Bring Your Own)</Text>
          <View style={styles.card}>
            <Text style={styles.cardDescription}>
              Bring your own API keys to use your preferred providers. Leave empty to use default keys.
              Keys are encrypted and stored securely.
            </Text>

            {loadingKeys ? (
              <ActivityIndicator size="large" color="#D4A574" style={{ marginTop: 20 }} />
            ) : (
              <>
                {renderProviderSection('Anthropic', 'anthropic', anthropic, setAnthropic)}
                {renderProviderSection('OpenAI', 'openai', openai, setOpenai)}
                {renderProviderSection('OpenRouter', 'openrouter', openrouter, setOpenrouter)}
              </>
            )}
          </View>
        </View>

        {/* Sign out */}
        <View style={styles.section}>
          <TouchableOpacity
            style={styles.signOutButton}
            onPress={() => router.replace('/(auth)/login')}
          >
            <Text style={styles.signOutButtonText}>Sign Out</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F3F0',
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
    color: '#0F0D0A',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#6B6358',
    fontStyle: 'italic',
  },
  content: {
    flex: 1,
  },
  section: {
    padding: 24,
    paddingTop: 16,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: '500',
    color: '#6B6358',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 12,
  },
  card: {
    backgroundColor: '#FDFCFB',
    borderWidth: 1,
    borderColor: 'rgba(212, 165, 116, 0.2)',
    borderTopWidth: 2,
    borderTopColor: '#D4A574',
    borderRadius: 2,
    padding: 20,
    gap: 16,
    shadowColor: '#0F0D0A',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 24,
    elevation: 4,
  },
  cardDescription: {
    fontSize: 14,
    color: '#6B6358',
    lineHeight: 20,
    marginBottom: 4,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  settingLabel: {
    fontSize: 16,
    color: '#0F0D0A',
  },
  settingValue: {
    fontSize: 16,
    color: '#6B6358',
  },
  settingValueMuted: {
    fontSize: 14,
    color: '#9B9388',
    fontStyle: 'italic',
  },
  providerSection: {
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#D1CCC4',
  },
  providerTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#0F0D0A',
    marginBottom: 12,
  },
  savedText: {
    fontSize: 14,
    color: '#4A7C59',
    marginBottom: 12,
  },
  inputContainer: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
  },
  input: {
    flex: 1,
    backgroundColor: '#F5F3F0',
    borderWidth: 1,
    borderColor: '#D1CCC4',
    borderRadius: 2,
    padding: 12,
    fontSize: 14,
    color: '#0F0D0A',
  },
  showButton: {
    backgroundColor: '#F5F3F0',
    borderWidth: 1,
    borderColor: '#D1CCC4',
    borderRadius: 2,
    paddingHorizontal: 16,
    justifyContent: 'center',
  },
  showButtonText: {
    fontSize: 12,
    fontWeight: '500',
    color: '#6B6358',
    textTransform: 'uppercase',
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 8,
  },
  button: {
    flex: 1,
    padding: 12,
    borderRadius: 2,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 44,
  },
  saveButton: {
    backgroundColor: '#D4A574',
  },
  saveButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#FDFCFB',
    textTransform: 'uppercase',
  },
  testButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#D4A574',
  },
  buttonText: {
    fontSize: 12,
    fontWeight: '500',
    color: '#D4A574',
    textTransform: 'uppercase',
  },
  deleteButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#A05A52',
  },
  deleteButtonText: {
    fontSize: 12,
    fontWeight: '500',
    color: '#A05A52',
    textTransform: 'uppercase',
  },
  signOutButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#A05A52',
    borderRadius: 2,
    padding: 14,
    alignItems: 'center',
  },
  signOutButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#A05A52',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
});
