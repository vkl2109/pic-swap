import { StyleSheet, View, Pressable, Text, TextInput } from 'react-native';

export default function CreateRoom({ navigation }) {
    return (
        <View style={styles.buttonContainer}>
            <TextInput
                style={styles.textInput}
                placeholder="Room Name"
                maxLength={20}
            />
            <Pressable style={styles.button} onPress={() => navigation.navigate('LandingPage')}>
                <Text style={styles.buttonLabel}>Enter the Room</Text>
            </Pressable>
        </View>
    );
}

const styles = StyleSheet.create({
    buttonContainer: {
        width: 320,
        height: 68,
        marginHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 3,
    },
    button: {
        borderRadius: 10,
        width: '100%',
        height: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
    },
    buttonIcon: {
        paddingRight: 8,
    },
    buttonLabel: {
        color: '#fff',
        fontSize: 16,
    },
    textInput: {
        borderColor: '#CCCCCC',
        borderTopWidth: 1,
        borderBottomWidth: 1,
        height: 50,
        fontSize: 25,
        paddingLeft: 20,
        paddingRight: 20
    }
});