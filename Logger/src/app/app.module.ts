import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './main/login/login.component';
import { LogviewComponent } from './main/logview/logview.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AnomalyComponent } from './main/anomaly/anomaly.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    LogviewComponent,
    AnomalyComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
