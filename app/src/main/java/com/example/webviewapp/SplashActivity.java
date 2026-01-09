package com.example.webviewapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class SplashActivity extends AppCompatActivity {

    private static final int SPLASH_DURATION = 2000; // 2秒

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        ImageView logoImageView = findViewById(R.id.logoImageView);
        TextView appNameTextView = findViewById(R.id.appNameTextView);

        // Logo渐隐渐现动画
        Animation fadeIn = AnimationUtils.loadAnimation(this, R.anim.fade_in);
        logoImageView.startAnimation(fadeIn);

        // 应用名称延迟显示并渐显
        new Handler().postDelayed(() -> {
            appNameTextView.animate().alpha(1.0f).setDuration(1000).start();
        }, 500);

        // 2秒后跳转到主界面
        new Handler().postDelayed(() -> {
            Intent intent = new Intent(SplashActivity.this, MainActivity.class);
            startActivity(intent);
            finish();
            
            // 添加退出动画
            Animation fadeOut = AnimationUtils.loadAnimation(this, R.anim.fade_out);
            overridePendingTransition(0, android.R.anim.fade_out);
        }, SPLASH_DURATION);
    }
}
