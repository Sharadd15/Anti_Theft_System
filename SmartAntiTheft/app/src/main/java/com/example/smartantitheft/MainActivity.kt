package com.example.smartantitheft

import android.app.Dialog
import android.content.BroadcastReceiver
import android.content.Context
import android.graphics.drawable.ColorDrawable
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.Window
import android.widget.ImageView
import android.widget.RelativeLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.gms.tasks.Task
import com.google.firebase.auth.AuthResult
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.QuerySnapshot
import com.google.firebase.storage.FileDownloadTask
import com.google.firebase.storage.FirebaseStorage
import com.google.firebase.storage.StorageTask
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.alert_list_item.view.*
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

private const val TAG = "FirebaseConn"

class Alert(val date: Date, val location: String)

class AlertViewHolder(view: View) : RecyclerView.ViewHolder(view) {
    val alertDate = view.alert_date
    val alertLocation = view.alert_location
}

class AlertAdapter(private val context: Context) :
    RecyclerView.Adapter<AlertViewHolder>() {

    private val textFmt = SimpleDateFormat("DD.MM.yyyy HH:mm")
    private val imgFmt = SimpleDateFormat("yyyy-MM-DD HH:mm:ss")

    init {
        imgFmt.timeZone = TimeZone.getTimeZone("UTC")
    }

    var items = listOf<Alert>()
        set(value) {
            field = value
            notifyDataSetChanged()
        }

    override fun getItemCount() = items.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AlertViewHolder {
        return AlertViewHolder(
            LayoutInflater.from(context).inflate(
                R.layout.alert_list_item,
                parent,
                false
            )
        )
    }

    override fun onBindViewHolder(holder: AlertViewHolder, position: Int) {
        val alert = items[position]
        holder?.alertDate?.text = alert.date.toLocaleString()
        holder?.alertLocation?.text = alert.location
        holder.itemView.setOnClickListener {

            val localFile = File.createTempFile("images", "jpg")
            val imageName = imgFmt.format(alert.date)
            Log.d(TAG, imageName)

            downloadImage(imageName, localFile)
                .addOnSuccessListener {

                    val builder = Dialog(this.context)
                    builder.requestWindowFeature(Window.FEATURE_NO_TITLE)
                    builder.window?.setBackgroundDrawable(
                        ColorDrawable(android.graphics.Color.TRANSPARENT)
                    )
                    val imageView = ImageView(this.context)
                    imageView.setImageURI(Uri.fromFile(localFile))
                    builder.addContentView(
                        imageView,
                        RelativeLayout.LayoutParams(
                            ViewGroup.LayoutParams.MATCH_PARENT,
                            ViewGroup.LayoutParams.MATCH_PARENT
                        )
                    )

                    builder.show()
                }
        }
    }

    private fun downloadImage(
        fileName: String,
        localFile: File
    ): StorageTask<FileDownloadTask.TaskSnapshot> {
        val storage = FirebaseStorage.getInstance()
        val imgRef = storage.reference.child("$fileName.jpg")
        return imgRef.getFile(localFile)
            .addOnSuccessListener {
            }.addOnFailureListener {
                Log.w(TAG, it.localizedMessage)
            }
    }
}

class MainActivity : AppCompatActivity() {

    companion object {
        lateinit var instance: MainActivity
    }

    private lateinit var adapter: AlertAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        instance = this

        alert_list.layoutManager = LinearLayoutManager(this)
        adapter = AlertAdapter(this)
        alert_list.adapter = adapter

        authenticateUser().addOnSuccessListener {
            connectDB()
        }

        swipe_container.setOnRefreshListener {
            connectDB().addOnCompleteListener {
                swipe_container.isRefreshing = false
            }
        }
    }

    private fun authenticateUser(): Task<AuthResult> {
        val auth = FirebaseAuth.getInstance()
        return auth.signInWithEmailAndPassword("test@test.com", "test123")
            .addOnSuccessListener {
                Log.d(TAG, "Logged in as ${it.user.email}")
            }
    }

    fun connectDB(): Task<QuerySnapshot> {
        val db = FirebaseFirestore.getInstance()
        return db.collection("alerts")
            .get()
            .addOnSuccessListener { query ->
                for (document in query) {
                    Log.d(TAG, "${document.id} => ${document.data}")
                }
                adapter.items = query
                    .map { entry ->
                        Alert(
                            entry.data["timestamp"] as Date,
                            entry.data["location"] as String
                        )
                    }
                    .sortedByDescending { alert -> alert.date }
            }.addOnFailureListener {
                Log.w(TAG, it.localizedMessage)
            }
    }
}
