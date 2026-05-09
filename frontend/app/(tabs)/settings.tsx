import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';

export default function SettingsScreen() {
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

        {/* API Keys section (BYOK - to be implemented) */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>API Keys</Text>
          <View style={styles.card}>
            <Text style={styles.cardDescription}>
              Bring your own API keys to use your preferred providers. Leave empty to use default keys.
            </Text>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Anthropic</Text>
              <Text style={styles.settingValueMuted}>Not configured</Text>
            </View>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>OpenAI</Text>
              <Text style={styles.settingValueMuted}>Not configured</Text>
            </View>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>OpenRouter</Text>
              <Text style={styles.settingValueMuted}>Not configured</Text>
            </View>
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
    borderColor: 'rgba(212, 165, 116, 0.2)', // primary-500/20
    borderTopWidth: 2,
    borderTopColor: '#D4A574', // primary-500
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
  signOutButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#A05A52', // error-500
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
