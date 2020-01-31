package com.example.smartantitheft

import android.util.Log
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage


class MyFirebaseMessagingService : FirebaseMessagingService() {
    override fun onMessageReceived(message: RemoteMessage) {
        Log.d("FirebaseConn", "message received")
        MainActivity.instance.connectDB()
    }

    override fun onNewToken(token: String) {
        Log.d("FirebaseConn", token)
        val db = FirebaseFirestore.getInstance()
        db.collection("users")
            .document("testuser")
            .set(mapOf("token" to token))
    }
}
