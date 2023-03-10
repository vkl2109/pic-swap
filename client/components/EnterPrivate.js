import { StyleSheet, SafeAreaView, ScrollView, View, Pressable, Text, TextInput } from 'react-native';
import { useState, useEffect } from 'react'
import { Button } from '@rneui/themed';
import AsyncStorage from '@react-native-async-storage/async-storage';


export default function EnterPrivate({ navigation, socket, loginData }) {

    const [name, onChangeName] = useState('')

    const handleSubmit = async () => {

        let req = await fetch(`http://10.129.2.90:5000/rooms/${name}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${await AsyncStorage.getItem('token')}`
            }
        })
        let res = await req.json()
        console.log(res)
    }


    // useEffect(() => {
    //     socket.on('join_success', (room) => {
    //         console.log(room.message)
    //         navigation.navigate('PaintRoom', { roomID: room.message });
    //     });
    // }, [socket])

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center' }}>
                <View style={styles.buttonContainer}>
                    <TextInput
                        style={styles.textInput}
                        placeholder="Room Name"
                        placeholderTextColor="rgba(300, 300, 300, 0.3)"
                        maxLength={20}
                        value={name}
                        onChangeText={onChangeName}
                    />
                    <Button
                        title="Enter Room"
                        titleStyle={{ fontWeight: '700' }}
                        buttonStyle={{
                            backgroundColor: 'rgba(90, 154, 230, 1)',
                            borderColor: 'transparent',
                            borderWidth: 0,
                            borderRadius: 30,
                        }}
                        containerStyle={{
                            width: 200,
                            marginHorizontal: 50,
                            marginVertical: 10,
                        }}
                        onPress={() => handleSubmit()}
                    />
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5EA9D', // '#25292e'
        alignItems: 'center',
        justifyContent: 'center'
    },
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
        paddingRight: 20,
        marginVertical: 20
    }
});