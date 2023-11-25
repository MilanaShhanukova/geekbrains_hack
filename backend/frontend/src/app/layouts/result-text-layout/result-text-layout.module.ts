import { NgModule } from '@angular/core';
import { ResultTextLayoutComponent } from './result-text-layout.component';
import { MarkdownModule } from 'ngx-markdown';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import {
  NbButtonModule,
  NbCardModule,
  NbDialogModule,
  NbPopoverModule,
  NbTooltipModule,
} from '@nebular/theme';
import { TooltipComponent } from '../../components/tooltip/tooltip.component';

@NgModule({
  declarations: [ResultTextLayoutComponent, TooltipComponent],
  exports: [ResultTextLayoutComponent, TooltipComponent],
  imports: [
    NbTooltipModule,
    NbButtonModule,
    NbPopoverModule,
    NbCardModule,
    NbDialogModule.forChild(),

    CommonModule,
    MarkdownModule.forRoot(),
    RouterModule.forChild([
      {
        path: '',
        component: ResultTextLayoutComponent,
      },
    ]),
  ],
})
export class ResultTextLayoutModule {}
