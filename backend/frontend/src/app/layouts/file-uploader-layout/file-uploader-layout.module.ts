import { NgModule } from '@angular/core';
import { FileUploadModule } from '@iplab/ngx-file-upload';
import { FileUploaderComponent } from '../../components/file-uploader/file-uploader.component';
import { FileUploaderLayoutComponent } from './file-uploader-layout.component';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NbButtonModule, NbCardModule } from '@nebular/theme';
import { NbIconModule } from '@nebular/theme';
import { AudioRecognitionLoaderComponent } from '../../components/audio-recognition-loader/audio-recognition-loader.component';

@NgModule({
  imports: [
    CommonModule,
    FileUploadModule,
    ReactiveFormsModule,

    RouterModule.forChild([
      {
        path: '',
        component: FileUploaderLayoutComponent,
      },
    ]),

    NbIconModule,
    NbCardModule,
    NbButtonModule,
  ],
  declarations: [
    FileUploaderComponent,
    FileUploaderLayoutComponent,
    AudioRecognitionLoaderComponent,
  ],
  exports: [
    FileUploaderComponent,
    FileUploaderLayoutComponent,
    AudioRecognitionLoaderComponent,
  ],
})
export class FileUploaderLayoutModule {}
