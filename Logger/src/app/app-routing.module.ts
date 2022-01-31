import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnomalyComponent } from './main/anomaly/anomaly.component';
import { LoginComponent } from './main/login/login.component';
import { LogviewComponent } from './main/logview/logview.component';
const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {path: 'logview', component: LogviewComponent},
  {path: 'anomaly/:id', component: AnomalyComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
